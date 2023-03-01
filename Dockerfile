FROM python:3.11-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "script:app", "--host", "0.0.0.0", "--port", "80"]
