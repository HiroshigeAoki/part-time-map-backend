# Pull base image
FROM python:3.9

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV LANG C.UTF-8
ENV TZ Asia/Tokyo

WORKDIR /code/backend

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD [ "uvicorn", "api.main:app", "--reload","--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000