FROM python:3.12
WORKDIR /usr/src/cbr_bot
COPY . .

RUN python -m pip install --upgrade pip
RUN python -m pip install poetry
RUN python -m poetry install --without dev
