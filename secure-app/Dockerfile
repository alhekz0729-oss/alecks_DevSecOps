FROM python:3.12.2-slim AS builder

ENV PYTHONUNBUFFERED=1
WORKDIR /workspace
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12.2-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PATH=/install/bin:$PATH
RUN adduser --disabled-password --gecos "" appuser
WORKDIR /home/appuser/app
COPY --from=builder /install /install
COPY app ./app
USER appuser
EXPOSE 5000
CMD ["python", "-u", "app/main.py"]
