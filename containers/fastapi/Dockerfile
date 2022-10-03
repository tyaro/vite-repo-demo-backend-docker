FROM python:3.9
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm
ENV SECRET_KEY $SECRET_KEY

WORKDIR /root/opt
RUN apt-get install -y vim less
RUN apt-get install -y rsyslog
RUN apt-get install -y cron

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install fastapi uvicorn
RUN pip install sqlalchemy
RUN pip install pandas
RUN pip install aiofiles
RUN pip install openpyxl
RUN pip install Pillow
RUN pip install attrdict
RUN pip install passlib
RUN pip install alembic
RUN pip install psycopg2
RUN pip install python-jose
RUN pip install python-multipart

CMD uvicorn main:app --reload --host 0.0.0.0 --port 5433

EXPOSE 5433
