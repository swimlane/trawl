
FROM python:3.7-alpine as base
RUN pip install --upgrade pip
RUN apk add --update --no-cache g++ gcc libxslt-dev

WORKDIR /entrails
COPY entrails/ /entrails/
RUN pip install -r requirements.txt
RUN python setup.py install

FROM python:3.7-alpine
WORKDIR /
COPY --from=base /usr/local/lib/python3.7/site-packages/ /usr/local/lib/python3.7/site-packages/

WORKDIR /spotter
COPY spotter/ /spotter/

RUN pip install -r requirements.txt
RUN python setup.py install

CMD ["python", "-u", "./spotter/spotter.py"]




