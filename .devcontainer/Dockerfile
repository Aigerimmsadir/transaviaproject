# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /workspace
COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt && pip install pylint pydocstyle flake8 bandit yapf autopep8
COPY . /code/