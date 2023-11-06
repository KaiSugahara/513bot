FROM python:3.10.13
USER root

ENV TZ=Asia/Tokyo

# Install Libraries
RUN pip install --upgrade pip
RUN pip install arxiv openai pytz requests python-dotenv polars

# Change WORKDIR
WORKDIR /

# Scheduled execution
RUN apt update && apt -y install cron
RUN echo 'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin' >> /etc/cron.d/crontab
RUN echo "CRON_TZ=Asia/Tokyo" >> /etc/cron.d/crontab
RUN echo '00 9 * * * /usr/local/bin/python3 /crawling.py >> /log/crawling.log' >> /etc/cron.d/crontab
RUN echo '00 10-17 * * 1-6 /usr/local/bin/python3 /app.py >> /log/app.log' >> /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
CMD ["cron", "-f"]