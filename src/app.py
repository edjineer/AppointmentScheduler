from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from flask_restful import Api, Resource
from helpers import Doctor, printDrSchedule, isValidDateRequest
import pdb

app = Flask(__name__)
api = Api(app)

DRDICT = {}
CONFIRMED_APPTS = []
UNCONFIRMED_APPTS = []

swagger = Swagger(app)


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


class ReserveSlot(Resource):
    def post(self):
        """
        Request an appointment. Sample Valid Input is: {"patientName": "Aly","dateOfRequest": "2024-04-15", "timeOfRequest": "08:03", "appointmentSlot": {"day": "2024-05-02", "time": "08:00", "drName": "Jekyll"},
        ---
        responses:
          200:
            description: Success
          412:
            description: Violates 24 hour requirement
          500:
            description: Error
        """
        try:

            dataIn = request.get_json()
            print(dataIn)
            if not isValidDateRequest(dataIn):
                return {"message": "Reserved timeslot successfully"}, 412
            # Confirm that it is a valid request: Reservations must be made at least 24 hours in advance

            # Check for Conflicts
            return {"message": "Reserved timeslot successfully"}, 200
        except:
            return {"message": "Error clearing Dr Availability"}, 500


api.add_resource(SubmitDrAvailability, "/submit")
api.add_resource(GetDrAvailability, "/openings")
api.add_resource(ClearAllDrSchedules, "/clear")
api.add_resource(ReserveSlot, "/reserve")


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
