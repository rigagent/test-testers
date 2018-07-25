# Integration test suite for Bikes Tester Exercise
This project allows to set up isolated Docker environment for run integration test suite for Bikes Tester Exercise inside of Docker containers.

## Assumptions made in implementation
- User has **Linux** (Ubuntu preferable) OS as a host system
- **Preconditions** described in appropriate section are met
- Steps described in **Running tests** section are met

## Stack of used technologies:
- [Python 2.7](https://www.python.org/download/releases/2.7/) as a programming language
- [Selenium with Python](http://selenium-python.readthedocs.io/) as a WEB automation framework
- [unittest](https://docs.python.org/2/library/unittest.html) as a tests runner
- [Docker](https://www.docker.com) as an infrastructure manager
- [Docker Compose](https://docs.docker.com/compose/) as a tool for defining and running multi-container Docker applications
- [SeleniumHQ/docker-selenium](https://github.com/SeleniumHQ/docker-selenium) as a [Selenium Grid](https://www.seleniumhq.org/docs/07_selenium_grid.jsp)
- [Ubuntu 16.04](https://hub.docker.com/_/ubuntu/) - as a Operation System used in Docker conteiners

## Preconditions
To get started you need to ensure you have this tools installed on your local PC:
- **git**
- **docker-compose** (to be able to use this testing, you need to have Docker engine release `1.13.0+`. A simple way to check: `docker-compose -v`. You can find how to reinstall for needed version [here](https://docs.docker.com/compose/install/))
- also probably you need to fix Docker's **networking DNS config** for correct work with Docker (you can find how to do it [here](https://development.robinwinslow.uk/2016/06/23/fix-docker-networking-dns/))

## Running tests
Testing happens only in [Google Chrome](https://www.google.com/chrome/) browser.

To start testing you need to follow next steps:

- Clone the repository:
```bash
git clone https://github.com/rigagent/test-testers.git
```
- Go to the folder with docker compose file:
```bash
cd test-testers/testing_app/
```
- Then, run tests:
```bash
docker-compose up --abort-on-container-exit --timeout 5
```
This command runs the Selenium Grid with `chrome` browser, deploy test "Bikes Tester Exercise" application and executes the tests in parallel. The tests are going to connect to a remote driver.

Use `docker-compose down` to destroy the environment.