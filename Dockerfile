# Pull base image
FROM python:3.9

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV LANG C.UTF-8
ENV TZ Asia/Tokyo

WORKDIR /code/backend

# Setup python venv
RUN python -m venv venv
RUN . /code/backend/venv/bin/activate
RUN pip install --upgrade pip

# Install dependencies
COPY requirements.txt .
RUN  pip install -r requirements.txt
COPY . .

EXPOSE 8000