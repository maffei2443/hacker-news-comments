#!/bin/bash

scrapyd &
echo "$(pwd)" >> /home/deploy.log

cd /usr/src/app/tutorial
scrapyd-deploy 
cron -f  && tail -f /var/log/cron.log
