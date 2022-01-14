
FROM python:3.7-alpine as base
RUN pip3 install --upgrade pip
RUN apk add --update --no-cache g++ gcc libxslt-dev

WORKDIR /bones
COPY bones/ /bones/
RUN pip3 install -r requirements.txt
RUN python3 setup.py install

FROM python:3.7-alpine
WORKDIR /
COPY --from=base /usr/local/lib/python3.7/site-packages/ /usr/local/lib/python3.7/site-packages/

ENV TZ="America/Chicago"

WORKDIR /spotter
COPY spotter/ /spotter/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python3 setup.py install

CMD ["python3", "-u", "./spot.py"]
