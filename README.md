# Message Broker Deployed To Heroku

## Description

An API Gateway like that provides an external interface to the connected docker services as message brokers. The application as a fully installed Gitlab CI/ CD pipeline that builds, tests, statically analyses the codes quality and deploys the application to Heroku.  The system is done in a TDD Manner. 
Programming Language used: Python.
Testing Framework: Pytest. 
Orchestration of the services: Docker, Docker-Compose. 
Pipeline: Gitlab CI/ CD. 


## Pipeline Description:


![plot](pipeline.PNG)


## The application running on Heroku as service:

Heroku is used as a Paas solution for deploying the application. 
Only the master branch is staged for deployment.

![plot](heroku.PNG)



 ## Running the system Locally: 

 ```
1. Clone the system from CLI with: git clone   https://gitlab.com/Ahmed-Gebril/message-broker-deployed-to-heroku.git
2. Navigate to the download directory.
3. Run the command ‘docker-compose build -d –no-cache.’ And wait for the services to be built.
4. Run the command ‘docker-compose up.’ 
5. Inspect if the services are running with ‘docker ps.’ 
```
## Viewing the Endpoints

Viewing the messages: http://host.docker.internal:8080/api/messages. <br />
Viewing the logs: http://host.docker.internal:8080/api/run-log. <br />
Viewing node statistics: http://host.docker.internal:8080/api/node-statistic. <br />
Viewing queue statistics: http://host.docker.internal:8080/api/queue-statistic. <br />


## Running Unit and API tests:

The tests are already run in the pipeline in the Test stage. To ensure that the tests pass locally accepted change the occurrences of ‘172.19.0.1’ and ‘host.docker.internal’ to ‘localhost.’
```
-	Run the command ‘pytest.’

```
