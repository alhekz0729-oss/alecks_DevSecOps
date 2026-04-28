FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
RUN adduser --disabled-password --gecos "" appuser
WORKDIR /home/appuser

COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

COPY app ./app
USER appuser
EXPOSE 5000
CMD ["python", "-u", "app/main.py"]
