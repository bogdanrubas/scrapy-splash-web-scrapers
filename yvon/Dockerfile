FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app
RUN pip3 install --no-cache-dir -r requirements.txt

#ENTRYPOINT ["scrapy"]

CMD ["scrapy","crawl", "firstRun"]