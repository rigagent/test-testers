FROM ubuntu:18.04

WORKDIR /testing_app
COPY . .
RUN apt-get update -qq && apt-get install -y python-pip && chmod +x /testing_app/entrypoint.sh
RUN pip install selenium

ENTRYPOINT ["/testing_app/entrypoint.sh"]