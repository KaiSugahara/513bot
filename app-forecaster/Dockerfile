FROM python:3.10.13
USER root

ENV TZ=Asia/Tokyo

# Install Libraries
RUN pip install --upgrade pip
RUN pip install requests python-dotenv

# Change WORKDIR
WORKDIR /

# Scheduled execution (every morning at 9:00)
RUN apt update && apt -y install cron
RUN echo 'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin' >> /etc/cron.d/crontab
RUN echo "CRON_TZ=Asia/Tokyo" >> /etc/cron.d/crontab
RUN echo '00 09 * * 1-6 /usr/local/bin/python3 /app.py > /tmp.log' >> /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
CMD ["cron", "-f"]