# Appointment Scheduler

## Context  

This application is a side project to create a basic back-end scheduling service that supports two types of clients: patients and physicians.

## Instructions to Run  

1. Set up the Environment by running ```conda env create -f environment.yml```, and run it with ```conda activate ApptScheduler```


## Assumptions and Tradeoffs in the Design

### Requirement 1

Allows providers to submit times they are available for appointments.

* Assumes Drs have already been created and stored
* Assumes given start and end times do not overlap
* Assumes only one dr request at a time

### Requirement 2

Allows a client to retrieve a list of available appointment slots. Appointment Slots are 15 minutes long.

### Requirement 3

Allows clients to reserve an available appointment slot.

* User can only reserve one slot per endpoint call


### Requirement 4

* A

## Next Steps

* Add a Create Dr Endpoint
* Improve the Documentation of each endpoint with Swagger
* Use Data Transfer Objects


## References and Tools Used

### Tools

* Postman for Testing
* Swagger for documentation
* Black VSCode Extension for Python Linting

### References

* Swagger Set up: https://diptochakrabarty.medium.com/flask-python-swagger-for-rest-apis-6efdf0100bd7
* Refresher Tutorial for Flask: https://www.youtube.com/watch?v=GMppyAPbLYk
* Learning the Python Schedule Library: https://www.geeksforgeeks.org/python-schedule-library/
* Datetime Tutorial: https://www.w3schools.com/python/python_datetime.asp