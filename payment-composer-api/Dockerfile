FROM python:3.12 as builder

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM builder as development

RUN apt -q update && \
    apt install netcat-traditional -y && \
    curl -sSL https://raw.githubusercontent.com/eficode/wait-for/master/wait-for --output wait-for && \
    chmod +x wait-for && \
    mv wait-for /usr/bin/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]


FROM python:3.12 as production

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY --from=builder /app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
