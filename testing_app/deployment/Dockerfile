# to build docker image for test application deployment
FROM centos:latest

WORKDIR /app
RUN yum install -y git
RUN git clone https://github.com/rigagent/test-testers.git
ENTRYPOINT ["/app/test-testers/testing_app/deployment/entrypoint.sh"]