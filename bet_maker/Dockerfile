FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5055

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5055", "--reload"]
