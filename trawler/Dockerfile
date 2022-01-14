FROM python:3.6-alpine

WORKDIR /

COPY bones/requirements.txt bones/
RUN pip install --upgrade pip
RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN pip install -r /bones/requirements.txt
COPY bones/ /bones/
WORKDIR /bones/
RUN export PYTHONPATH=/bones/:$PYTHONPATH
RUN python setup.py install


WORKDIR /
COPY trawler/requirements.txt /
RUN pip install --upgrade pip
RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN pip install -r /requirements.txt
COPY trawler/ /
WORKDIR /
RUN export PYTHONPATH=/:$PYTHONPATH
RUN python setup.py install



CMD ["python", "-u", "consumer.py"]