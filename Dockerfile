
FROM python:3.12.0

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN mkdir /Django_Streaming_and_OEE/

WORKDIR /Django_Streaming_and_OEE

RUN pip install --upgrade pip

COPY requirements.txt /Django_Streaming_and_OEE/

RUN pip install -r requirements.txt

COPY . /Django_Streaming_and_OEE/

EXPOSE 8000

CMD ./manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000
