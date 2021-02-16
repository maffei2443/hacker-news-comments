FROM python:3.8-buster

RUN apt-get update -y \
    && apt-get install -y cron \
    && apt-get install -y nano

ENV CLOSESPIDER_ITEMCOUNT=0  
ENV CLOSESPIDER_PAGECOUNT=0
ENV CLOSESPIDER_TIMEOUT=0
ENV CONCURRENT_REQUESTS_PER_DOMAIN=30

WORKDIR /usr/src/app
COPY . .

RUN pip install -r requirements.txt

ENV FLASK_APP server.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000

# RUN apt-get update -y \
#     # && apt-get install utils\
#     && apt-get install software-properties-common -y \
#     && apt-get install -y poppler-utils \
#     && apt-get install -y locales && locale-gen en_US.UTF-8







# COPY crontab /etc/cron.d/crontab
# RUN chmod 0644 /etc/cron.d/crontab

RUN crontab -l 2>/dev/null; echo "*/1 * * * * echo $(date) >> /home/log.txt" | crontab -


# RUN service cron start

# CMD ["bash"]

# ENTRYPOINT service cron start && bash
CMD ["flask", "run"]

