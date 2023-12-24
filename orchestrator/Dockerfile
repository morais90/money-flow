FROM python:3.11 as builder

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

CMD ["python", "-m", "app.main"]


FROM python:3.12 as production

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

WORKDIR /app

COPY --from=builder /app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD ["python", "-m", "app.main"]
