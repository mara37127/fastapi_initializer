FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /app

COPY src/requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/src

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]