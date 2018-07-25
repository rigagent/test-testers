# to build docker image for application testing
FROM ubuntu:16.04

WORKDIR /testing_app
COPY . .
RUN apt-get update -qq && apt-get install -y python-pip
RUN pip install selenium
ENTRYPOINT ["/testing_app/entrypoint.sh"]