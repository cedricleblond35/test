# syntax=docker/dockerfile:1
FROM python:3.8

#RUN apt-get update
#RUN apt-get install ffmpeg libsm6 libxext6  -y

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt



COPY ./app/ ./app

CMD [ "python3", "./app/app.py"]