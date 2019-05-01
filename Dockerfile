FROM mpsamurai/neochi-dev-base:20190424-raspbian

COPY ./requirements.txt /tmp

RUN pip3 --no-cache-dir install -r /tmp/requirements.txt && rm /tmp/requirements.txt

#RUN apk add bind-tools

WORKDIR /code
COPY ./src .

#CMD ["wget", "https://bootstrap.pypa.io/get-pip.py"]
#CMD ["python", "get-pip.py"]
#CMD ["pip", "--no-cache-dir", "install", "-r", "/tmp/requirements.txt"]
#CMD ["rm", "/tmp/requirements.txt"]

#CMD ["nosetests", "--with-coverage", "--cover-html", "--cover-package", "ir-sender"]
#CMD ["nosetests", "--with-coverage", "--cover-html", "--cover-package", "neochi"]

CMD ["python3", "main.py"]