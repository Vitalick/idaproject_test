FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/idaproject_test

COPY . .
RUN pip install -r req.txt

EXPOSE 8000