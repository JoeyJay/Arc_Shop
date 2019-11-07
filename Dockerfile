FROM python:3

USER root

RUN apt-get update

RUN pip install \
  pandas \
  SQLAlchemy \
  urllib \
  pymssql \
  cryptography \
  re \
  uuid \
  random \
  datetime \

ADD /arc.py /
