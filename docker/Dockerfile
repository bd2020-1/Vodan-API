FROM python:3.8.6-slim-buster AS builder

WORKDIR /app

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/venv/bin:$PATH"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential mariadb-client libmariadbclient-dev && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /venv

COPY requirements.txt ./

RUN python3 -m pip install --no-cache-dir -r requirements.txt

FROM python:3.8.6-slim-buster

ENV PATH="/venv/bin:$PATH"

WORKDIR /app

EXPOSE 8000

CMD ["python3", "main.py"]

COPY --from=builder /venv /venv

COPY ./src/ ./