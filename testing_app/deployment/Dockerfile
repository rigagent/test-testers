# to build docker image for test application deployment
FROM ubuntu:16.04

WORKDIR /app
RUN apt-get update -qq && apt-get install -y python-pip git
RUN git clone https://github.com/rigagent/test-testers.git
ENTRYPOINT ["/app/test-testers/testing_app/deployment/entrypoint.sh"]