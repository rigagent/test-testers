# to build docker image for test application deployment
FROM centos:latest

WORKDIR /app
RUN yum install -y git
RUN git clone https://github.com/rigagent/test-testers.git
# RUN chmod +x /app/entrypoint.sh
# ENTRYPOINT ["/app/entrypoint.sh"]