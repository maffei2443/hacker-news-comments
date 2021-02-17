#!/bin/bash

# crontab -l 2>/dev/null
# echo "*/1 * * * * /usr/bin" | crontab -
# service cron start
# echo "Entry point was ran!" >> ran.txt
# ufw disable
echo -e "$(env)\n$(cat /etc/cron.d/simple)" >> /tmp/simple
mv /tmp/simple /etc/cron.d/simple
chmod 0644 /etc/cron.d/simple

rsyslogds
# service cron stop
# service cron force-reload 
# cron start
cron -f -L15 | tail -f /var/log/syslog
# flask run
