# WGUPS Routing Program, by Raymond Baartmans ID #001973555

import hub
import hash
import utils

done = False

print("WGUPS Routing Program, by Raymond Baartmans")
print(
    f"The total distance for all trucks for the day (9/10/2022) was { round(hub.calculateDeliveries(10), 2) } miles.")

# Time Complexity: O(N + N^2) (For each time user views package data)
# Space Complexity: O(N)
while not done:
    # receive user input, loop until user quits
    print("\nEnter [1] to view a specific package at a certain time")
    print("Enter [2] to view all packages at a certain time")
    print("Enter [3] to quit.")
    userInput = input()
    if userInput == "1":
        packageID = input(
            "Enter the ID of the package you would like to track:")
        try:
            # make sure package ID corresponds to a package in the hash table
            packageExists = hub.getHashTable().search(packageID)
            if packageExists == None:
                print("There is no package with that ID.")
            else:
                hour = input("Enter hour (Use 24-Hour Time):")
                minute = input("Enter minute:")
                try:
                    time = utils.convertToTime(int(hour), int(minute))
                    try:
                        print(
                            f"\nStatus for package with ID { packageID } at { time }:")
                        # calculate status of all packages at the time the user specified
                        totalMileage = hub.calculateDeliveries(
                            utils.convertToHours(time))
                        # retrieve the information of the specific package the user requested
                        pkg = hub.getHashTable().search(packageID)
                        # print package status
                        utils.printPackageInfo(pkg)
                        print(
                            f"\nTotal Miles Traveled by Both Trucks at { time }: {round(totalMileage, 2)}")
                    except:
                        print("Unknown Error.")
                except:
                    # user time input did not include a valid hour or minute
                    print("Invalid Input. Please enter a valid hour and minute.")
        except:
            # user time input did not include a valid ID number
            print("Invalid Input. Please enter a valid ID number.")
    elif userInput == "2":
        hour = input("Enter hour (Use 24-Hour Time):")
        minute = input("Enter minute:")
        try:
            time = utils.convertToTime(int(hour), int(minute))
            try:
                print(f"Status for all packages at { time }:")
                # calculate status of all packages at the time the user specified
                totalMileage = hub.calculateDeliveries(
                    utils.convertToHours(time))
                # retrieve all packages and print out their status
                packages = hub.getHashTable().getAllPackages()
                for pkg in packages:
                    utils.printPackageInfo(pkg)
                print(
                    f"\nTotal Miles Traveled by Both Trucks at { time }: {round(totalMileage, 2)}")
            except:
                print("Unknown Error.")
        except:
            # user time input did not include a valid hour or minute
            print("Invalid Input. Please enter a valid hour and minute.")
    elif userInput == "3":
        done = True
    else:
        print("Invalid Input. Please try again.")
