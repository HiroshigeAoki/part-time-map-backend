#!/bin/bash

apt-get update
apt-get -y install cron
crontab -l | { cat; echo "0 3 * * * bash /code/backend/crawl.sh"; } | crontab -
cron

uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload &
bash crawl.sh &
wait
