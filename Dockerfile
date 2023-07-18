FROM ubuntu:20.04
WORKDIR /app

RUN apt-get --allow-releaseinfo-change update
RUN apt update && apt-get install python3 python3-pip -y

ADD . .
RUN pip3 install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["app.py"]
