FROM python:latest
USER root

# INSTALL LIBRARY(S)
RUN pip3 install --upgrade pip
RUN pip3 install flask requests

# CHANGE WORKDIR
WORKDIR /

# CHANGE CMD
CMD ["python3", "app.py"]