import datetime
from datetime import timedelta

# time each truck leaves the hub
FIRST_TRUCK_START_TIME = datetime.datetime(2022, 9, 10, 8, 0, 0)
SECOND_TRUCK_START_TIME = datetime.datetime(2022, 9, 10, 9, 5, 0)
THIRD_TRUCK_START_TIME = datetime.datetime(2022, 9, 10, 10, 20, 0)

# constants for 2nd and 3rd truck (how many hours after the first truck leaves at 8am)
SECOND_TRUCK_OFFSET = abs(SECOND_TRUCK_START_TIME -
                          FIRST_TRUCK_START_TIME).total_seconds() / 3600
THIRD_TRUCK_OFFSET = abs(THIRD_TRUCK_START_TIME -
                         FIRST_TRUCK_START_TIME).total_seconds() / 3600


# O(1)
def formatTime(timeElapsed):
    # convert number of hours after 8am to a readable date
    return FIRST_TRUCK_START_TIME + timedelta(hours=timeElapsed)


# O(1)
def convertToHours(dateTime):
    # convert a date to number of hours after am
    if dateTime < FIRST_TRUCK_START_TIME:
        return 0.0
    hours = abs(dateTime - FIRST_TRUCK_START_TIME).total_seconds() / 3600
    return hours


# O(1)
def convertToTime(hour, min):
    # return a date given an hour and minute
    return datetime.datetime(2022, 9, 10, hour, min, 0)


# O(1)
def printPackageInfo(pkg):
    # print out package details in a readable format
    print("ID: " + pkg[0] + " | Delivery Address: " + pkg[1] + ", " + pkg[2] + ", " +
          pkg[3] + ", " + pkg[4] + " | Deadline: " + pkg[5] + " | Weight: " + pkg[6] + " | Status: " + pkg[8])
