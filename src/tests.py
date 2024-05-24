import unittest
import requests
from helpers import timeSplitter
from flask import jsonify
import pdb

BASE = "http://127.0.0.1:5000/"


class EndpointTests(unittest.TestCase):

    def test_requirement1(self):
        # Initialize App
        response = requests.delete(BASE + "clear")
        self.assertEqual(response.status_code, 200)

        # TODO: Test Malformed Data

        # Test 404
        req1In = {
            "name": "JekyllYYYYYYY",
            "times": [
                {"day": "2024-05-01", "startTime": "08:00", "endTime": "15:00"},
                {"day": "2024-05-02", "startTime": "08:00", "endTime": "15:00"},
                {"day": "2024-05-03", "startTime": "08:00", "endTime": "15:00"},
            ],
        }
        response = requests.post(BASE + "submit", json=req1In)
        self.assertEqual(response.status_code, 404)

        # Test Success
        req2In = {
            "name": "Jekyll",
            "times": [
                {"day": "2024-05-01", "startTime": "08:00", "endTime": "15:00"},
                {"day": "2024-05-02", "startTime": "08:00", "endTime": "15:00"},
                {"day": "2024-05-03", "startTime": "08:00", "endTime": "15:00"},
            ],
        }
        response = requests.post(BASE + "submit", json=req2In)
        self.assertEqual(response.status_code, 202)

    def test_requirement2(self):
        # Initialize App
        response = requests.delete(BASE + "clear")
        self.assertEqual(response.status_code, 200)

        # Init the DB with some data
        req2In1 = {
            "name": "Jekyll",
            "times": [
                {"day": "2024-05-01", "startTime": "08:00", "endTime": "09:00"},
            ],
        }
        response = requests.post(BASE + "submit", json=req2In1)
        self.assertEqual(response.status_code, 202)

        req2In2 = {
            "name": "Jekyll",
            "times": [
                {"day": "2024-05-02", "startTime": "12:00", "endTime": "13:00"},
            ],
        }
        response = requests.post(BASE + "submit", json=req2In2)
        self.assertEqual(response.status_code, 202)

        req2In3 = {
            "name": "DrA",
            "times": [
                {"day": "2024-05-02", "startTime": "12:00", "endTime": "13:00"},
            ],
        }
        response = requests.post(BASE + "submit", json=req2In3)
        self.assertEqual(response.status_code, 202)

        # Test the Output
        expectedOut = {
            "availability": [
                {
                    "name": "Jekyll",
                    "times": [
                        {"day": "2024-05-01", "time": "08:00"},
                        {"day": "2024-05-01", "time": "08:15"},
                        {"day": "2024-05-01", "time": "08:30"},
                        {"day": "2024-05-01", "time": "08:45"},
                        {"day": "2024-05-02", "time": "12:00"},
                        {"day": "2024-05-02", "time": "12:15"},
                        {"day": "2024-05-02", "time": "12:30"},
                        {"day": "2024-05-02", "time": "12:45"},
                    ],
                },
                {
                    "name": "DrA",
                    "times": [
                        {"day": "2024-05-02", "time": "12:00"},
                        {"day": "2024-05-02", "time": "12:15"},
                        {"day": "2024-05-02", "time": "12:30"},
                        {"day": "2024-05-02", "time": "12:45"},
                    ],
                },
                {"name": "DrB", "times": []},
                {"name": "DrC", "times": []},
                {"name": "DrD", "times": []},
                {"name": "DrE", "times": []},
            ]
        }

        response = requests.get(BASE + "openings")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expectedOut)

    # Test the 24 hour time window
    def test_requirement3a(self):
        # Initialize App
        response = requests.delete(BASE + "clear")
        self.assertEqual(response.status_code, 200)
        req3InitJekyll = {
            "name": "Jekyll",
            "times": [
                {"day": "2024-05-01", "startTime": "08:00", "endTime": "10:00"},
            ],
        }
        response = requests.post(BASE + "submit", json=req3InitJekyll)
        self.assertEqual(response.status_code, 202)

        # Reject Bc Too Close to actual date
        req3In1 = {
            "patientName": "Bob",
            "dateOfRequest": "2024-05-01",
            "timeOfRequest": "08:00",
            "appointmentSlot": {
                "day": "2024-05-01",
                "time": "08:00",
                "drName": "Jekyll",
            },
        }
        response = requests.post(BASE + "reserve", json=req3In1)
        self.assertEqual(response.status_code, 412)

        # Reject Bc Too Close to actual date
        req3In2 = {
            "patientName": "Boo",
            "dateOfRequest": "2024-05-01",
            "timeOfRequest": "08:03",
            "appointmentSlot": {
                "day": "2024-05-02",
                "time": "08:00",
                "drName": "Jekyll",
            },
        }
        response = requests.post(BASE + "reserve", json=req3In2)
        self.assertEqual(response.status_code, 412)

    # # Test the 24 hour time window
    # def test_requirement3General(self):
    #     # Initialize App
    #     response = requests.delete(BASE + "clear")
    #     self.assertEqual(response.status_code, 200)
    #     req3InitJekyll = {
    #         "name": "Jekyll",
    #         "times": [
    #             {"day": "2024-05-01", "startTime": "08:00", "endTime": "10:00"},
    #         ],
    #     }
    #     response = requests.post(BASE + "submit", json=req3InitJekyll)
    #     self.assertEqual(response.status_code, 202)

    #     # Basic Case
    #     req3In2 = {
    #         "patientName": "Aly",
    #         "dateOfRequest": "2024-04-15",
    #         "timeOfRequest": "08:03",
    #         "appointmentSlot": {
    #             "day": "2024-05-02",
    #             "time": "08:00",
    #             "drName": "Jekyll",
    #         },
    #     }
    #     response = requests.post(BASE + "reserve", json=req3In2)
    #     self.assertEqual(response.status_code, 202)

    # def test_r4(self):
    #     print("r4")
    #     pass

    # def test_a1(self):
    #     print("a1")
    #     pass

    # def test_a2(self):
    #     print("a2")
    #     pass


class HelperUnitTests(unittest.TestCase):
    def test_timeSplitter(self):

        # Simple Case
        start1 = "08:00"
        end1 = "09:15"
        out1 = ["08:00", "08:15", "08:30", "08:45", "09:00"]
        self.assertEqual(timeSplitter(start1, end1), out1)

        # Round Case, and PM
        start2 = "13:01"
        end2 = "14:14"
        out2 = ["13:15", "13:30", "13:45"]
        self.assertEqual(timeSplitter(start2, end2), out2)

        pass

    # def test_dayBefore(self):
    #     print("TST")
    #     pass

    # def test_expiration(self):
    #     print("TST")
    #     pass


if __name__ == "__main__":
    unittest.main()
