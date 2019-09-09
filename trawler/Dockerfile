FROM python:3.6-alpine

WORKDIR /

COPY entrails/requirements.txt entrails/
RUN pip install --upgrade pip
RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN pip install -r /entrails/requirements.txt
COPY entrails/ /entrails/
WORKDIR /entrails/
RUN export PYTHONPATH=/entrails/:$PYTHONPATH
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