from hash import DeliveriesHashTable
from utils import SECOND_TRUCK_OFFSET, THIRD_TRUCK_OFFSET, formatTime
import copy
import csv
NUMBER_OF_TRUCKS = 3
with open('./packages.csv') as packages:

    # populate hashtable with package data
    # Time Complexity: O(N)
    # Space Complexity: O(N)
    packageData = csv.reader(packages, delimiter=',')
    hashTable = DeliveriesHashTable()
    deliveries = []
    for i in range(0, NUMBER_OF_TRUCKS):
        deliveries.append([])
    for row in packageData:
        package = [row[0], row[1], row[2], row[3], row[4], row[5],
                   row[6], row[7], 'At Hub']
        # manage special requirements for certain packages
        if int(package[0]) in [13, 14, 15, 16, 19, 20]:
            # these all have to be on the same truck
            deliveries[0].append(package)
        elif package[0] == '9':
            # incorrect info, move to final truck which departs at 10:20 (after correct info is received)
            package[1] = '410 S State St'
            package[4] = '84111'
            deliveries[2].append(package)
        elif package[7] == "Can only be on truck 2" or "Delayed" in package[7]:
            deliveries[1].append(package)
        elif package[5] != 'EOD':
            # There is a delivery deadline, put on first truck to be delivered as early as possible
            deliveries[0].append(package)
        else:
            # spread the rest of the packages evenly between the second and third delivery
            if len(deliveries[1]) < len(deliveries[2]):
                deliveries[1].append(package)
            else:
                deliveries[2].append(package)
        # insert package into the hashtable
        hashTable.insert(package[0], package[1], package[2], package[3],
                         package[4], package[5], package[6], package[7], 'At Hub')

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def getHashTable():
        return hashTable

    # Time Complexity: O(N)
    # Space Complexity: O(1)
    def resetAllPackages():
        for i in range(1, 41):
            pkg = hashTable.search(str(i))
            pkg[8] = "At Hub"
            hashTable.update(i, pkg)

    # Time Complexity: O(N)
    # Space Complexity: O(1)
    def setEnRoute(package):
        # Set a package's status to en route
        package[8] = "En Route"
        hashTable.update(package[0], package)

    # Time Complexity: O(N)
    # Space Complexity: O(1)
    def setDelivered(package, time):
        # Set a package's status to delivered, along with the time of delivery
        package[8] = "Delivered: " + \
            str(formatTime(time))
        hashTable.update(package[0], package)

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def getDeliveries():
        return deliveries


with open('./distances.csv') as distances:
    distanceData = list(csv.reader(distances, delimiter=','))
    sortedTrucks = [[], [], []]

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def getTime(distance):
        time = distance / 18
        return time

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def getDistance(location1, location2):
        # get the distance between two locations from the distance CSV file
        for i in range(1, len(distanceData)):
            # search for address in table matching first location
            if location1 in distanceData[i][0]:
                for j in range(2, len(distanceData) + 1):
                    # search for address in table matching second location
                    if location2 in distanceData[0][j]:
                        # if the distance doesnt exist or is 0.0, the number is located at the opposite location between the two locations
                        if distanceData[i][j] == '0.0' or distanceData[i][j] == '':
                            return float(distanceData[j - 1][i + 1])
                        return float(distanceData[i][j])

    # Time Complexity: O(N)
    # Space Complexity: O(N)
    def deliverNextPackage(sortedTruck, currentLocation, currentTime, endTime):
        # delivers the first package in the sortedTruck array

        # get distance between current location and the place the next package has to be delivered
        distance = getDistance(currentLocation, sortedTruck[0][1])
        nextLocation = sortedTruck[0][1]
        # amount of time it will take to reach destination
        addedTime = getTime(distance)
        if (currentTime + addedTime) > endTime:
            # the truck is not able to reach its next destination before the stop time, return
            return (-1.0, currentLocation)
        # deliver the package, and pop it from the sorted truck array
        setDelivered(sortedTruck[0], currentTime + addedTime)
        sortedTruck.pop(0)
        # return the distance traveled and the new current location
        return (distance, nextLocation)

    # Time Complexity: O(N^2)
    # Space Complexity: O(N)
    def orderPackages(truckPackages, truckNumber, location):
        if not truckPackages:
            # packages have been ordered
            return
        nearest = 15.0  # distance of nearest location
        lowIndex = 0  # index of package that has the nearest distance
        currentLocation = location
        # find package with closest address to current location
        for i in range(len(truckPackages)):
            distance = getDistance(truckPackages[i][1], location)
            if distance <= nearest:
                nearest = distance
                lowIndex = i
                currentLocation = truckPackages[i][1]
        # add package to ordered list of packages, pop from unordered list
        sortedTrucks[truckNumber].append(truckPackages[lowIndex])
        truckPackages.pop(lowIndex)
        orderPackages(truckPackages, truckNumber, currentLocation)

    # Time Complexity: O(1)
    # Space Complexity: O(1)
    def calculateDistanceRemaining(distance, timeElapsed, endTime):
        # calculate how far the truck has traveled in between locations if the end time is before all packages are delivered, or the travel distance back to the hub
        # how many extra miles the truck can travel in the time remaining
        milesLeft = (endTime - timeElapsed) * 18
        if milesLeft < distance and milesLeft > 0:
            return milesLeft
        elif distance < milesLeft and distance > 0:
            return distance
        else:
            return 0.0

    # Time Complexity: O(N^2 + N)
    # Space Complexity: O(N)
    # Runs trucks until the specified end time, which is represented in number of hours after 8AM (when the trucks leave)
    def calculateDeliveries(endTime):
        # make a copy of the deliveries object so the deliveries can be calculated an unlimited amount of times
        deliveriesCopy = copy.deepcopy(getDeliveries())
        resetAllPackages()  # reset all package status, this is necessary for when the user requests package status multiple times
        totalDistance = 0.0
        if endTime <= 0.0:  # the specified end time was before any of the trucks leave
            return totalDistance
        # calculate package status for each truck
        for i in range(0, NUMBER_OF_TRUCKS):
            # set starting location to wgups hub
            currentLocation = '4001 South 700'
            timeElapsed = 0.0
            if i == 1:
                timeElapsed = SECOND_TRUCK_OFFSET  # equivalent to 9:05 am
            elif i == 2:
                timeElapsed = THIRD_TRUCK_OFFSET  # equivalent to 10:20 am
            if timeElapsed < endTime:
                # if there is time for the truck to depart, run the algorithm to make a delivery path
                orderPackages(deliveriesCopy[i], i, currentLocation)
                for package in sortedTrucks[i]:
                    # set all packages en route
                    setEnRoute(package)
                # while the truck still has packages, keep making deliveries
                while sortedTrucks[i]:
                    if timeElapsed > endTime:  # if the end time has been passed, stop
                        break
                    # deliver package
                    result = deliverNextPackage(
                        sortedTrucks[i], currentLocation, timeElapsed, endTime)
                    if result[0] == -1.0:
                        # Time ran out before package was delivered
                        break
                    # update total distnace, time elapsed, and current location after delivery was made
                    totalDistance += result[0]
                    timeElapsed += getTime(result[0])
                    currentLocation = result[1]
            # calculate how much trucks traveled in between locations before end time
            if not sortedTrucks[i] and not deliveriesCopy[i]:
                # deliveries finished, send truck back to hub
                returnDistance = getDistance(
                    currentLocation, '4001 South 700')
                totalDistance += calculateDistanceRemaining(
                    returnDistance, timeElapsed, endTime)
            elif sortedTrucks[i] and not deliveriesCopy[i]:
                # deliveries were not finished, calculate how far truck has traveled in between locations
                returnDistance = getDistance(
                    currentLocation, sortedTrucks[i][0][1])
                totalDistance += calculateDistanceRemaining(
                    returnDistance, timeElapsed, endTime)
            sortedTrucks[i].clear()

        return totalDistance
