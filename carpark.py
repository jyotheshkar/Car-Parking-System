

import csv
from datetime import datetime as DT
import re
import random

class ParkingSpaceNode:
    def __init__(self, space_id):
        self.space_id = space_id
        self.next = None

class CarParkingSystem:
    def __init__(self):
        self.car_parking_spaces = 7
        self.csv_file = 'parkingRecords.csv'
        self.head = None  # Linked list head for parking spaces
        self.car_parking_records = []
        self.csv_titles = ["Registration Number", "Ticket Number", "Parking ID Number", "Entry Time", "Exit Time", "Parking Fee"]
        self.loadParkingRecords()
        self.initializeParkingSpaces()

    def loadParkingRecords(self):
        try:
            with open(self.csv_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip headers
                self.car_parking_records = [row for row in reader]
        except FileNotFoundError:
            pass

    def initializeParkingSpaces(self):
        self.head = ParkingSpaceNode(1)
        current = self.head
        for i in range(2, self.car_parking_spaces + 1):
            new_node = ParkingSpaceNode(i)
            current.next = new_node
            current = new_node

    def getAvailableSpaces(self):
        available_spaces = []
        current = self.head
        while current:
            available_spaces.append(current.space_id)
            current = current.next
        return available_spaces

    def createParkingSpace(self):
        occupied_spaces = [int(record[2]) for record in self.car_parking_records]
        available_spaces = self.getAvailableSpaces()
        return random.choice(list(set(available_spaces) - set(occupied_spaces)))

    def isCarInParking(self, registration_number):
        for record in self.car_parking_records:
            if record[0] == registration_number and record[4] == "Parking...":
                return True
        return False

    def enterCarPark(self):
        while True:
            registration_number = input("Enter your Car Registration number (Enter United Kingdom Registration number for Cars. Example format is LA07EDC): ")
            if self.authentication(registration_number):
                if self.isCarInParking(registration_number):
                    print("Car with this registration is already parked.")
                else:
                    break
            else:
                print("Invalid registration format. Please enter a valid UK-based registration number")

        parking_space = self.createParkingSpace()
        if parking_space:
            entry_time = DT.now()
            time_format = entry_time.strftime("%Y-%m-%d %H:%M:%S.%f")
            ticket_generator = self.generateParkingID(registration_number)

            self.car_parking_records.append([registration_number, ticket_generator, f"{parking_space}", entry_time.strftime("%Y-%m-%d %H:%M:%S.%f"), "Parking...", "Parking..."])

            print("Vehicle entered the car park successfully")
            print(f"Vehicle Registration Number: {registration_number}")
            print(f"Parking ID Number: {ticket_generator}")
            print(f"Parking Space ID: {parking_space}")
            print(f"Entry Time: {time_format}")
            remaining_car_spaces = self.car_parking_spaces - len(self.car_parking_records)
            print(f"Remaining parking slots: {remaining_car_spaces}")
            self.writeParkingRecords()
        else:
            print("Car park is full")

    def generateParkingID(self, registration_number):
        number_logic = [str(random.randint(0, 9)) for _ in range(4)]
        random_numbers = ''.join(number_logic)
        letters_logic = [random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(2)]
        random_letters = ''.join(letters_logic)
        return f"{random_numbers}{random_letters}{registration_number}"

    def authentication(self, registration_number):
        registration_pattern = re.compile(r'^[A-Z]{2}\d{2}[A-Z]{3}$')
        return bool(re.match(registration_pattern, registration_number))

    def writeParkingRecords(self):
        with open(self.csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.csv_titles)  # Write CSV titles
            writer.writerows(self.car_parking_records)

    def exitCarPark(self):
        registration_number = input("Enter your Car's Registration Number: ")
        exit_time = DT.now()
        car_matched = False

        for car_record in self.car_parking_records:
            if car_record[0] == registration_number and car_record[4] == "Parking...":
                entry_time_str = car_record[3]  # Get entry time as string from record
                entry_time = DT.strptime(entry_time_str, "%Y-%m-%d %H:%M:%S.%f")  # Convert to datetime
                total_parking_time = exit_time - entry_time
                parking_fee = self.calculateFee(total_parking_time)

                # Update the record with exit time and parking fee
                car_record[4] = exit_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                car_record[5] = round(parking_fee, 2)

                print("Car has exited the car parking successfully")
                print(f"Exit time: {exit_time}")
                print(f"Parking fee: £{parking_fee}")

                car_matched = True
                break

        if car_matched:
            self.writeParkingRecords()
        else:
            print("Vehicle record not found")

    def calculateFee(self, duration):
        total_parking_hours = duration.total_seconds() / 3600
        parking_fee = total_parking_hours * 2
        return round(parking_fee, 2)

    def availableParkingSpaces(self):
        occupied_spaces = [int(record[2]) for record in self.car_parking_records if record[4] == "Parking..."]
        accessible_spaces = self.getAvailableSpaces()
        remaining_spaces = len(list(set(accessible_spaces) - set(occupied_spaces)))
        print(f"Remaining parking spaces: {remaining_spaces}")

    def queryParkingRecords(self):
        ticket_generator = input("Enter your ticket number: ")
        for record in self.car_parking_records:
            if record[1] == ticket_generator:
                print("Parking record details:")
                print(f"Ticket Number: {record[1]}")
                print(f"Vehicle Registration Number: {record[0]}")
                print(f"Parking space ID: {record[2]}")
                print(f"Entry Time: {record[3]}")
                print(f"Exit Time: {record[4]}")
                print(f"Parking Fee: £{record[5]}")
                return

        print("Provided ticket number is invalid")

    def mainMenu(self):
        while True:
            print("Welcome to the Car Parking System")
            print("1. Enter the car park")
            print("2. Exit the car park")
            print("3. View available parking spaces")
            print("4. Query parking record by ticket number")
            print("5. Quit")

            selection = input("Please enter your choice: ")

            if selection == '1':
                self.enterCarPark()
            elif selection == '2':
                self.exitCarPark()
            elif selection == '3':
                self.availableParkingSpaces()
            elif selection == '4':
                self.queryParkingRecords()
            elif selection == '5':
                print("You have exited the car parking system. See you next time!")
                break
            else:
                print("Invalid choice. Kindly select a valid option.")

if __name__ == "__main__":
    parking_system = CarParkingSystem()
    parking_system.mainMenu()
