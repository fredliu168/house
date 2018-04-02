FROM python:3.6-alpine
ADD . /code
VOLUME /code/upload
WORKDIR /code
RUN apk update \
    && apk add --update --no-cache g++ gcc libxslt-dev==1.1.29-r1 \
    && apk add python3 curl \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py \
    && rm get-pip.py \
    && pip install -r requirements.txt

CMD ["python", "manage.py"]

EXPOSE 5000