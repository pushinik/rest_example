FROM python:3.12.10-alpine

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["fastapi", "run", "src/main.py"]
