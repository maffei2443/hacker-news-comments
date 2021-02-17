FROM python:3.8-buster

ENV CLOSESPIDER_ITEMCOUNT=0  
ENV CLOSESPIDER_PAGECOUNT=0
ENV CLOSESPIDER_TIMEOUT=0
ENV CONCURRENT_REQUESTS_PER_DOMAIN=30

WORKDIR /usr/src/app
COPY . .

RUN chmod +x /usr/src/app/entrypoint.sh
RUN pip install -r requirements.txt

ADD crontab /etc/cron.d/hello-cron
RUN chmod 0644 /etc/cron.d/hello-cron
# Create the log file to be able to run tail
RUN touch /var/log/cron.log

RUN apt-get update -y \
    && apt-get install -y cron \
    && apt-get install -y nano


ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
