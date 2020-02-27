FROM ubuntu:18.04

ENV WORKDIR /app
WORKDIR $WORKDIR

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    wget

RUN rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD python3 paper-qa-api.py