FROM python:3.11-slim

WORKDIR /app

COPY ../requirements.txt .
COPY ../src ./src
COPY ../data ./data
COPY ../scripts ./scripts

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]