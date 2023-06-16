## Table of contents
* [Introduction: Basic ETL process using Docker Compose](#Introduction)
* [Technologies](#technologies)
* [Requirements](#requirements)
* [Setup](#setup)

# Introduction: Basic ETL process using Docker Compose
This is a basic illustration of how to run python on a docker container, and execute scripts that extracts data from an api and loads to a containerised database- postgresDB. This is all bundled in a docker compose file.
 It reads api data from randam-data-api(https://random-data-api.com/api/v2/users) and populates the db tables below:
 1. postgres.staging.users_raw with raw data
 2. postgres.analytics.users with the transformed data

## Requirements
Host requirements (laptop, or VM), where you will be executing this program:
1. Install Docker Engine and Docker compose <br />
    To install docker:  https://docs.docker.com/engine/install/ <br />
    To install docker compose plugin: https://docs.docker.com/compose/install/linux/

2. Install git: https://github.com/git-guides/install-git

## Technologies
1. Docker and Docker compose
2. Postgres:13 and associated SQL scripts
3. Python 3.11-slim-buster

## Setup
1. Clone the repo git clone https://github.com/Ebuk-a/docker-etl-adhoc
2. Cd into the directory: cd docker-etl-adhoc
    Have a quick scan of the files within.
3. Run: docker compose up -d
4. Execute the python script on the app container: docker exec python-app python3 basic_etl.py  
5. This should print out some prompts and populate the database.
6. To confirm data has been writen, access the database using DB client(pgAdmin or any other) with the following connection details<br />
        Host: localhost<br />
        Database: postgres <br />
        User: postgres <br />
        Password: postgres
7. Check out both tables: <br />
        postgres.staging.users_raw <br />
        postgres.analytics.users <br />