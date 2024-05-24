from flask import Flask, request, jsonify
from flasgger import Swagger
from flask_restful import Api, Resource
from helpers import (
    Doctor,
    printDrSchedule,
    isValidDateRequest,
    isAvailableTimeSlot,
    Appointment,
    manageExpirations,
)
from datetime import datetime
import threading

# Number of Seconds before checking if there are unconfirmed Appts.
# It may be helpful to increase this value when testing
REFRESH_RATE = 10

app = Flask(__name__)
api = Api(app)

DRDICT = {}
CONFIRMED_APPTS = {}
UNCONFIRMED_APPTS = {}

swagger = Swagger(app)


# Cancel appointments if they were created over 30 minutes ago
def updateTime():
    threading.Timer(REFRESH_RATE, updateTime).start()
    currentTime = datetime.now()
    itemsToRemove = manageExpirations(DRDICT, UNCONFIRMED_APPTS, currentTime)
    for id in itemsToRemove:
        print(
            f"Appointment for {UNCONFIRMED_APPTS[id].patient} cancelled due to expiration."
        )
        UNCONFIRMED_APPTS.pop(id)


updateTime()


class SubmitDrAvailability(Resource):
    def post(self):
        """
        Submit a doctor's availability. Requires a name of a doctor who is already added into the database {name: str}, and a array  called "times" that contains days and time ranges in the format [{day: YYYY-MM-DD, startTime: HH:MM, endTime: HH:MM},...]
        ---
        responses:
          202:
            description: Successfully added availability
          404:
            description: Dr is not present in Dr Database
          500:
            description: Error Completing this request
        """
        try:
            dataIn = request.get_json()
            drName = dataIn.get("name")
            drTimes = dataIn.get("times")
            if drName not in DRDICT:
                return {"message": "Dr is not present in Dr Database"}, 404

            # Run it
            DRDICT[drName].addSlotsToWorkingSchedule(drTimes)

        except:
            return {"message": "Error Completing this request"}, 500

        return {"message": "Successfully added availability"}, 202


class GetDrAvailability(Resource):
    def get(self):
        """
        Get all doctor's availabilities.
        ---
        responses:
          200:
            description: Availability successfully added
        """
        outDict = printDrSchedule(DRDICT)
        return jsonify(outDict)


class ReserveSlot(Resource):
    def post(self):
        """
        Request an appointment. Sample Valid Input is: {"patientName": "Aly","dateOfRequest": "2024-04-15", "timeOfRequest": "08:03", "appointmentSlot": {"day": "2024-05-02", "time": "08:00", "drName": "Jekyll"},
        ---
        responses:
          202:
            description: Success
          412:
            description: Violates 24 hour requirement
          404:
            description: Appointment Slot Not found
          500:
            description: Error
        """
        try:
            dataIn = request.get_json()
            # Confirm that it is a valid request: Reservations must be made at least 24 hours in advance
            if not isValidDateRequest(dataIn):
                return {
                    "message": "Error: reservation must be made more than 24 hours in advance"
                }, 412
            # Confirm that all data is valid
            if not isAvailableTimeSlot(dataIn, DRDICT):
                return {"message": "Error: Dr or Timeslot does not exist"}, 404

            # Make Booking
            patientName = dataIn.get("patientName")
            drName = dataIn.get("appointmentSlot")["drName"]
            apptDate = dataIn.get("appointmentSlot")["day"]
            apptTime = dataIn.get("appointmentSlot")["time"]
            bookingStr = dataIn.get("dateOfRequest") + " " + dataIn.get("timeOfRequest")
            bookingObj = datetime.strptime(bookingStr, "%Y-%m-%d %H:%M")
            apptObj = Appointment(patientName, drName, bookingObj, apptDate, apptTime)
            UNCONFIRMED_APPTS[apptObj.id] = apptObj
            return {
                "message": f"Reserved timeslot successfully",
                "bookingID": f"{apptObj.id}",
            }, 202
        except:
            return {"message": "Error setting appointment"}, 500


class ConfirmSlot(Resource):
    def post(self):
        """
        Confirm an Appointment. Input is booking ID
        ---
        responses:
          200:
            description: Confirmation Successful
          404:
            description: Appointment Slot Not found
          500:
            description: Error
        """
        try:
            dataIn = request.get_json()
            id = dataIn.get("bookingID")
            # Confirm that it is a valid request: Reservations must be made at least 24 hours in advance
            if id not in UNCONFIRMED_APPTS:
                return {"message": "Booking not found"}, 404
            CONFIRMED_APPTS[id] = UNCONFIRMED_APPTS.pop(id)
            return {"message": "Confirmed"}, 200

        except:
            return {"message": "Error Confirming appointment"}, 500


# Utility Endpoint
class ClearAllDrSchedules(Resource):
    def delete(self):
        """
        Helper Call to clear the Dr Schedules. Useful for testing without resetting the app.
        ---
        responses:
          200:
            description: Cleared Dr Availability
          500:
            description: Error clearing Dr Availability
        """
        try:
            DRDICT.clear()
            initializeDrs()
            cleanList = printDrSchedule(DRDICT)
            return jsonify(cleanList)
        except:
            return {"message": "Error clearing Dr Availability"}, 500


api.add_resource(SubmitDrAvailability, "/submit")
api.add_resource(GetDrAvailability, "/openings")
api.add_resource(ClearAllDrSchedules, "/clear")
api.add_resource(ReserveSlot, "/reserve")
api.add_resource(ConfirmSlot, "/confirm")


def initializeDrs():
    DRDICT["Jekyll"] = Doctor("Jekyll")
    DRDICT["DrA"] = Doctor("DrA")
    DRDICT["DrB"] = Doctor("DrB")
    DRDICT["DrC"] = Doctor("DrC")
    DRDICT["DrD"] = Doctor("DrD")
    DRDICT["DrE"] = Doctor("DrE")


if __name__ == "__main__":
    initializeDrs()
    app.run(debug=True)
