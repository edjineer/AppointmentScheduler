# Appointment Scheduler

## Context  

This application is a side project to create a basic back-end scheduling service that supports two types of clients: patients and physicians.

## Instructions to Run  

1. Set up the Environment by running ```conda env create -f environment.yml```, and run it with ```conda activate ApptScheduler```
2. Run the application by running the command: ```python src/app.py```

### Testing

There are two options available for testing this API. For both of these options, make sure to run the app first.

1. A postman collection is available in the postman directory. You can import these into the Postman app to run one-off tests.
2. A Unit Test Suite can be run using the command ```python src/tests.py```


### Documentation

To view the Swagger auto-generated documentation for all endpoints, run the app and then visit the following URL in a web browser: http://127.0.0.1:5000/apidocs/

## Assumptions and Tradeoffs in the Design

### Requirement 1

Allows providers to submit times they are available for appointments.

* Assumes Drs have already been created and stored
* Assumes given start and end times do not overlap
* Assumes only one dr request at a time

### Requirement 2

Allows a client to retrieve a list of available appointment slots. Appointment Slots are 15 minutes long.

### Requirement 3

Allows clients to reserve an available appointment slot. Reservations must be made at least 24 hours in advance

* Assume user can only reserve one slot per endpoint call

### Requirement 4

Allows clients to confirm their reservation.

## Next Steps

* Add a "Create Dr" Endpoint
* Incorporate a more robust database into this app
* Improve the Documentation of each endpoint with Swagger
* Use Data Transfer Objects
* Incorporate unique IDs to drs and patients to avoid conflicts
* Build out a Client Class
* Improve the Confirmation system

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
* UUID Generation: https://www.uuidgenerator.net/dev-corner/python#google_vignette