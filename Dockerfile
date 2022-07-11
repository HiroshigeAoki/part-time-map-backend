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

CMD ["/bin/bash", "startup.sh"]
EXPOSE 8000