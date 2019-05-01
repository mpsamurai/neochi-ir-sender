FROM mpsamurai/neochi-dev-base:20190424-x64

COPY ./requirements.txt /tmp
RUN pip --no-cache-dir install -r /tmp/requirements.txt && rm /tmp/requirements.txt

WORKDIR /code
COPY ./src .

CMD ["nosetests", "--with-coverage", "--cover-html", "--cover-package", "ir-sender"]
CMD ["nosetests", "--with-coverage", "--cover-html", "--cover-package", "neochi"]
