FROM mpsamurai/neochi-dev-base:20190424-raspbian

COPY ./requirements.txt /tmp

RUN pip3 --no-cache-dir install -r /tmp/requirements.txt && rm /tmp/requirements.txt

#RUN apk add bind-tools

RUN mkdir -p /neochi/data/ir
#COPY ./data/0.ir /neochi/data/ir

WORKDIR /code
COPY ./src .

#CMD ["nosetests", "--with-coverage", "--cover-html", "--cover-package", "ir-sender"]
#CMD ["nosetests", "--with-coverage", "--cover-html", "--cover-package", "neochi"]

CMD ["python3", "main.py"]
#CMD ["python3", "sleep.py"]
#CMD ["python3", "kinesis.py"]
#CMD ["python3", "test_kinesis.py"]
