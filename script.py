from fastapi import FastAPI, Query, HTTPException
import uvicorn
import csv
from pydantic import BaseModel
from datetime import date, datetime, timedelta
from pytz import timezone

print("Please wait. The server is preparing data...")
app = FastAPI()


# Pedantic models for response data
class CityModel(BaseModel):
    geonameid: str
    name: str
    asciiname: str | None
    alternatenames: str | None
    latitude: str | None
    longitude: str | None
    feature_class: str | None
    feature_code: str | None
    country_code: str | None
    cc2: str | None
    admin1_code: str | None
    admin2_code: str | None
    admin3_code: str | None
    admin4_code: str | None
    population: str | None
    elevation: str | None
    dem: str | None
    timezone: str | None
    modification_date: date


class ListCityModel(BaseModel):
    cities_list: list[CityModel]


class TwoCitiesModel(ListCityModel):
    more_northerly: str
    timezone_coincidence: bool
    time_shifting: str


class AutoCompleteModel(BaseModel):
    list_of_variations: list[str]


class Cities:
    """Class for getting city data in different formats"""

    def __init__(self):
        self.model_keys = CityModel.__fields__.keys()     # Getting the fields of the city model
        # Retrieving a list, a dictionary of city models, and a set of city names
        self.cities = [CityModel(**dict(zip(self.model_keys, i))) for i in self.read_data_generator()]
        self.id_to_info = {info.geonameid: info for info in self.cities}
        self.name_set = {info.name for info in self.cities}

    # Generator for reading data from a file
    def read_data_generator(self) -> list:
        with open("RU.txt", "r") as file:
            read_data = csv.reader(file, delimiter="\t")
            for row in read_data:
                yield row

    def get_city_by_id(self, city_id: str) -> CityModel:
        exception = HTTPException(status_code=404, detail="City not found")
        response = self.id_to_info.get(city_id)
        if not response:
            raise exception
        else:
            return response

    # Getting the right number of elements on the right page
    def get_city_list(self, page_num: int, page_size: int) -> ListCityModel:
        id_start_shift = (page_num - 1) * page_size
        id_stop_shift = page_num * page_size - 1
        city_list = []
        for index, city in enumerate(self.cities):
            if id_start_shift <= index <= id_stop_shift:
                city_list.append(city)
        return ListCityModel(cities_list=city_list)

    # Getting information about two cities entered in Russian, getting the difference in time zones, checking the
    # coincidence of the time zone
    def get_two_cities(self, first_city: str, second_city: str) -> TwoCitiesModel:
        exception = HTTPException(status_code=404, detail="City not found")
        if first_city in cities.name_set and second_city in cities.name_set:
            first_city_data = max(self.cities, key=lambda x: x.name == first_city and int(x.population))
            second_city_data = max(self.cities, key=lambda x: x.name == second_city and int(x.population))
            more_northerly = max(first_city_data, second_city_data, key=lambda x: x.latitude).name
            current_time = datetime.utcnow()
            time_shifting = abs(timezone(first_city_data.timezone).utcoffset(current_time)
                                - timezone(second_city_data.timezone).utcoffset(current_time))
            timezone_coincidence = True if time_shifting == timedelta(days=0, hours=0, seconds=0) else False
            return TwoCitiesModel(cities_list=[first_city_data, second_city_data],
                                  more_northerly=more_northerly,
                                  timezone_coincidence=timezone_coincidence,
                                  time_shifting=str(time_shifting))
        else:
            raise exception


cities = Cities()


def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)


# Table for batch character replacement
letters = str.maketrans({
  'А': 'A',
  'Б': 'B',
  'В': 'V',
  'Г': 'G',
  'Д': 'D',
  'Е': 'E',
  'Ё': 'E',
  'Ж': 'Zh',
  'З': 'Z',
  'И': 'I',
  'Й': 'Y',
  'К': 'K',
  'Л': 'L',
  'М': 'M',
  'Н': 'N',
  'О': 'O',
  'П': 'P',
  'Р': 'R',
  'С': 'S',
  'Т': 'T',
  'У': 'U',
  'Ф': 'F',
  'Х': 'H',
  'Ц': 'Ts',
  'Ч': 'Ch',
  'Ш': 'Sh',
  'Щ': 'Sch',
  'Ъ': '',
  'Ы': 'Y',
  'Ь': '',
  'Э': 'E',
  'Ю': 'Yu',
  'Я': 'Ya',
  'а': 'a',
  'б': 'b',
  'в': 'v',
  'г': 'g',
  'д': 'd',
  'е': 'e',
  'ё': 'e',
  'ж': 'zh',
  'з': 'z',
  'и': 'i',
  'й': 'y',
  'к': 'k',
  'л': 'l',
  'м': 'm',
  'н': 'n',
  'о': 'o',
  'п': 'p',
  'р': 'r',
  'с': 's',
  'т': 't',
  'у': 'u',
  'ф': 'f',
  'х': 'h',
  'ц': 'ts',
  'ч': 'ch',
  'ш': 'sh',
  'щ': 'sch',
  'ъ': '',
  'ы': 'y',
  'ь': '`',
  'э': 'e',
  'ю': 'yu',
  'я': 'ya',
 })


@app.get("/city", response_model=CityModel)
def get_info_about_city(geonameid: int = Query(gt=0)):
    return cities.get_city_by_id(str(geonameid))


@app.get("/list-of-cities", response_model=ListCityModel)
def get_cities_list_with_info(page_num: int = Query(ge=1),
                              page_size: int = Query()):
    return cities.get_city_list(page_num, page_size)


@app.get("/two-cities", response_model=TwoCitiesModel)
def get_info_about_two_cities(
        first_city: str = Query(min_length=2, max_length=20),
        second_city: str = Query(min_length=2, max_length=20)
):
    first_city = first_city.translate(letters)          # Translation of Russian characters into transliteration
    second_city = second_city.translate(letters)

    return cities.get_two_cities(first_city, second_city)


@app.post("/autocomplete", response_model=AutoCompleteModel)
def autocomplete(string: str = Query(min_length=1, max_length=20)):
    list_of_variations = [name for name in cities.name_set if name.startswith(string)]
    return AutoCompleteModel(list_of_variations=list_of_variations)


if __name__ == "__main__":
    start_server()
