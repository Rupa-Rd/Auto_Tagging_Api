FROM python:3.11.4-slim

ENV PYTHONUNBUFFERED True

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
RUN apt install -y libgl1-mesa-glx -y

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 AutoTagApi:app