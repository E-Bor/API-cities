# Get started
Before starting, you must install all the necessary packages. To do this, run the command:

`pip install -r requirements.txt`

The next step you need to put the file "RU.txt" in the project directory "/InfotecsTest"

At the end, you can run the project with the command:

`python3 script.py`

The running server will be available at http://127.0.0.1:8000.  

***Please wait 10-15 seconds for the server to prepare the data.***

### Description of methods

Autodocumentation is available at http://127.0.0.1:8000/docs.

#### /city
The method accepts the city geonameid value as the url parameter. The method returns a dictionary with information about
the city. Dictionary field names match the format of the provided data in the "RU.txt" file.

Usage example: `http://127.0.0.1:8000/city?geonameid=451747`

Response body example: 

```{
  "geonameid": "451747",
  "name": "Zyabrikovo",
  "asciiname": "Zyabrikovo",
  "alternatenames": "",
  "latitude": "56.84665",
  "longitude": "34.7048",
  "feature_class": "P",
  "feature_code": "PPL",
  "country_code": "RU",
  "cc2": "",
  "admin1_code": "77",
  "admin2_code": "",
  "admin3_code": "",
  "admin4_code": "",
  "population": "0",
  "elevation": "",
  "dem": "204",
  "timezone": "Europe/Moscow",
  "modification_date": "2011-07-09"
}
```

#### /list-of-cities

The method receives two url parameters as input. 1 - page_num (number of the page to display) 2 - page_size (number of 
elements to display on the desired page). The method returns a dictionary. In the dictionary by the key "cities_list" 
you can get a list of cities data. The city data format is the same as in the previous method.

Usage example: `http://127.0.0.1:8000/list-of-cities?page_num=1&page_size=2`

Response body example:

```{
  "cities_list": [
    {
      "geonameid": "451747",
      "name": "Zyabrikovo",
      "asciiname": "Zyabrikovo",
      "alternatenames": "",
      "latitude": "56.84665",
      "longitude": "34.7048",
      "feature_class": "P",
      "feature_code": "PPL",
      "country_code": "RU",
      "cc2": "",
      "admin1_code": "77",
      "admin2_code": "",
      "admin3_code": "",
      "admin4_code": "",
      "population": "0",
      "elevation": "",
      "dem": "204",
      "timezone": "Europe/Moscow",
      "modification_date": "2011-07-09"
    },
    {
      "geonameid": "451748",
      "name": "Znamenka",
      "asciiname": "Znamenka",
      "alternatenames": "",
      "latitude": "56.74087",
      "longitude": "34.02323",
      "feature_class": "P",
      "feature_code": "PPL",
      "country_code": "RU",
      "cc2": "",
      "admin1_code": "77",
      "admin2_code": "",
      "admin3_code": "",
      "admin4_code": "",
      "population": "0",
      "elevation": "",
      "dem": "215",
      "timezone": "Europe/Moscow",
      "modification_date": "2011-07-09"
    }
  ]
}
```

#### /two-cities

The method receives two url parameters as input. 1 - first_city 2 - second_city. Both parameters are city names. Names
can be written in Russian, or in transliteration, as in the file "RU.txt". The method returns a dictionary. 

By the key "cities_list" a list with information about cities is available. The data format is the same as in the first method.

The key "more_northerly" returns the name of a more northerly city.

By the key "timezone_coincidence", a match of time zones is returned (True - if they match, False - differ).

The "time_shifting" key shows how much the time zones of the two cities differ 

***_Implemented the first additional task!_***

Usage example: `http://127.0.0.1:8000/two-cities?first_city=Moskva&second_city=Tomsk`

or if in russian: `http://127.0.0.1:8000/two-cities?first_city=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0&second_city=%D0%A2%D0%BE%D0%BC%D1%81%D0%BA`

Response body example:

```
{
  "cities_list": [
    {
      "geonameid": "524900",
      "name": "Moskva",
      "asciiname": "Moskva",
      "alternatenames": "Krasnaya Moskva,Moskva,Москва",
      "latitude": "56.91775",
      "longitude": "32.16579",
      "feature_class": "P",
      "feature_code": "PPL",
      "country_code": "RU",
      "cc2": "",
      "admin1_code": "77",
      "admin2_code": "511588",
      "admin3_code": "",
      "admin4_code": "",
      "population": "17",
      "elevation": "",
      "dem": "245",
      "timezone": "Europe/Moscow",
      "modification_date": "2019-08-30"
    },
    {
      "geonameid": "1489425",
      "name": "Tomsk",
      "asciiname": "Tomsk",
      "alternatenames": "TOF,Tom'sku,Tomck,Tomium,Toms'k,Tomsk,Tomska,Tomskaj,Tomskas,Tomszk,Tomçk,tomseukeu,tomska,tomusuku,tuo mu si ke,twmsk,twmsq,Τομσκ,Томск,Томскай,Томськ,Томьскъ,Տոմսկ,טומסק,تومسك,تومسک,ٹومسک,तोम्स्क,トムスク,托木斯克,톰스크",
      "latitude": "56.49771",
      "longitude": "84.97437",
      "feature_class": "P",
      "feature_code": "PPLA",
      "country_code": "RU",
      "cc2": "",
      "admin1_code": "75",
      "admin2_code": "1489419",
      "admin3_code": "",
      "admin4_code": "",
      "population": "574002",
      "elevation": "",
      "dem": "117",
      "timezone": "Asia/Tomsk",
      "modification_date": "2022-10-16"
    }
  ],
  "more_northerly": "Moskva",
  "timezone_coincidence": false,
  "time_shifting": "4:00:00"
}
```

#### /autocomplete

Method from the second additional task.
It takes a string as a transliteration. Returns a dictionary. By the key "list_of_variations" you can get a list of cities. 
The names of these cities begin with the entered string.

Usage example: `http://127.0.0.1:8000/autocomplete?string=Moskv`


Response body example: 
```
{
  "list_of_variations": [
    "Moskva Kurgan",
    "Moskvitsy",
    "Moskvinka",
    "Moskvitino",
    "Moskvikha",
    "Moskvina",
    "Moskvinskoye",
    "Moskvinskaya",
    "Moskvin Pochinok",
    "Moskvino",
    "Moskvorech’ye-Saburovo",
    "Moskvyata",
    "Moskvorechye-Saburovo District",
    "Moskvoretsksya Sloboda",
    "Moskva",
    "Moskvichi"
  ]
}
```
