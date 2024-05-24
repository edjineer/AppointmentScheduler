from datetime import datetime, timedelta
import pdb

APPT_INTERVAL = 15


class Doctor:
    def __init__(self, name):
        self.name = name
        self.workingDays = {}  # Key = Date, Value = Object
        ##TODO: Add unique ID in case of Dr Conflicts

    # Requires an array of dictionaries {day:"YYYY-MM-DD", startTime: "HH:MM", endTime: "HH:MM"}
    # Assumes no conflicting time slots given
    def addSlotsToWorkingSchedule(self, inputArray):
        for slot in inputArray:
            givenDay = slot["day"]
            if givenDay in self.workingDays:
                self.workingDays[givenDay].addAvailability(
                    slot["startTime"], slot["endTime"]
                )
            else:
                newDayObj = WorkingDay(givenDay)
                newDayObj.addAvailability(slot["startTime"], slot["endTime"])
                self.workingDays[givenDay] = newDayObj

    def getFreeTimes(self):
        returnArray = []
        for day in self.workingDays.values():
            for time in day.openTimes:
                returnArray.append({"day": day.date, "time": time})
        return returnArray


class WorkingDay:
    def __init__(self, dateStr):
        self.date = dateStr
        self.openTimes = []
        self.bookedTimes = []

    def addAvailability(self, startStrTime, endStrTime):
        newSlots = timeSplitter(startStrTime, endStrTime)
        self.openTimes.extend(newSlots)
        self.openTimes.sort()


class Appointment:
    def __init__(self, patientName, drName, bookingTime, apptDate, apptTime):
        self.patient = patientName
        self.dr = drName
        self.appointmentDate = apptDate  # Should be YYYY-MM-DD
        self.appointmentTime = apptTime  # Should be HH:MM
        self.bookingTime = bookingTime  # Will Be full datetimeOjb


# Utility to print all Drs Schedules
def printDrSchedule(inDict):
    outList = []
    for dr in inDict.values():
        tmpDrOut = {}
        tmpDrOut["name"] = dr.name
        tmpDrOut["times"] = dr.getFreeTimes()
        outList.append(tmpDrOut)
    outDict = {"availability": outList}
    return outDict


# Data in is of the format: {"patientName": "Aly","dateOfRequest": "2024-04-15", "timeOfRequest": "08:03", "appointmentSlot": {"day": "2024-05-02", "time": "08:00", "drName": "Jekyll"}
# Return false if it violates the 24 hours requirement
def isValidDateRequest(dataIn):
    requestStr = dataIn.get("dateOfRequest") + " " + dataIn.get("timeOfRequest")
    requestDateObj = datetime.strptime(requestStr, "%Y-%m-%d %H:%M")
    apptData = dataIn.get("appointmentSlot")
    apptStr = apptData["day"] + " " + apptData["time"]
    apptDateObj = datetime.strptime(apptStr, "%Y-%m-%d %H:%M")
    timeDifference = apptDateObj - requestDateObj
    if timeDifference.days > 0:
        return True
    return False


# Data in is of the format: {"patientName": "Aly","dateOfRequest": "2024-04-15", "timeOfRequest": "08:03", "appointmentSlot": {"day": "2024-05-02", "time": "08:00", "drName": "Jekyll"}
# Return false if appointment slot does not exist
def isAvailableTimeSlot(dataIn, drDict):
    drName = dataIn.get("appointmentSlot")["drName"]
    if drName not in drDict:
        return False
    date = dataIn.get("appointmentSlot")["day"]
    if date not in drDict[drName].workingDays:
        return False
    time = dataIn.get("appointmentSlot")["time"]
    if time not in drDict[drName].workingDays[date].openTimes:
        return False
    return True


# Input: 2 strings: start time and end time in HH:MM format
# Output: Array of intervals
# Requirement: Intervals of 15 mins
def timeSplitter(startTime, endTime):
    # Convert to a datetime readable format to do algebra on
    rawStartTime = datetime.strptime(startTime, "%H:%M")
    rawEndTime = datetime.strptime(endTime, "%H:%M")

    # Round up the start time's minutes
    if rawStartTime.minute % APPT_INTERVAL > 0:
        correctionValSt = APPT_INTERVAL - (rawStartTime.minute % APPT_INTERVAL)
        fixedMinuteSt = rawStartTime.minute + correctionValSt
        fixedStartTime = rawStartTime.replace(minute=fixedMinuteSt)
    else:
        fixedStartTime = rawStartTime

    # Round down the end time's minutes
    if rawEndTime.minute % APPT_INTERVAL > 0:
        correctionValEnd = rawEndTime.minute % APPT_INTERVAL
        fixedMinuteEnd = rawEndTime.minute - correctionValEnd
        fixedEndTime = rawEndTime.replace(minute=fixedMinuteEnd)
    else:
        fixedEndTime = rawEndTime

    # Fill Array List with times
    returnArray = []
    timeItr = fixedStartTime  # Confirmed that this is a deep copy
    while timeItr < fixedEndTime:
        readableVal = timeItr.strftime("%H:%M")
        returnArray.append(readableVal)
        timeItr += timedelta(minutes=APPT_INTERVAL)

    return returnArray
