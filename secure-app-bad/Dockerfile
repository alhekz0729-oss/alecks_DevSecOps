FROM python:3.8-buster

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt
COPY app ./app
EXPOSE 5000
CMD ["python", "app/main.py"]
