# ISU Calendar Generator
## A web application that generates an .ics calendar file for ISU classes

## Steps to Run from Terminal
- cd into ISUCalendarGen
- make sure you have .env file to connect to remote postgresql instance (don't push this file to git)
- if you're using a virtualenv, active it (run `source venv/bin/activate`)
- install dependencies by running `pip install -r requirements.txt`
- cd into src/ 
- run `flask run`


## Steps to run locally with Docker compose
- cd into ISUCalendarGen
- run `make docker-build`

### What's happening in docker-build? Look in Makefile:
- run `docker compose up -d db`
- run `docker compose up --build flaskapp`

### You can view the database within the docker container as well:
- run `docker exec -it db psql -U postgres`
- run `\dt` to see all tables
- run `\d calendar` to see columns/info on calendar table
- run `select * from calendar;` to see all rows in calendar table

### To clean up all the docker stuff (you should do this to rebuild everything)
- run `make docker-clean`

The following is what's happening when you run the make command:
- if flask app is still running hit Control+C to stop it 
- run `docker ps -a` to see all containers
- run `docker stop flaskapp`
- run `docker rm flaskapp`
- look at the output of `docker ps -a` and get the CONTAINER ID for postgres:12 (this changes each time you build the docker container)
- run `docker stop <insert CONTAINER ID of postgres:12>`
- run `docker rm <insert CONTAINER ID of postgres:12>`
- run `docker volume prune -f` (this deletes db data)

### If you're on Windows and don't have make
- install package manager Chocolatey if you don't have it: https://chocolatey.org/install#individual
- run `choco install make`

### If you don't have Docker
- install docker here: https://docs.docker.com/get-docker/
