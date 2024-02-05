
import tkinter as tk
from datetime import datetime as DT
from carpark import CarParkingSystem

class ParkingSpaceNode:
    def __init__(self, space_id):
        self.space_id = space_id
        self.next = None

class CarParkingGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Parking System")
        self.parking_system = CarParkingSystem()

        self.label = tk.Label(master, text="Welcome to the Car Parking System")
        self.label.pack()

        self.enter_button = tk.Button(master, text="Enter the car park", command=self.enter_car_park)
        self.enter_button.pack()

        self.exit_button = tk.Button(master, text="Exit the car park", command=self.exit_car_park)
        self.exit_button.pack()

        self.view_button = tk.Button(master, text="View available parking spaces", command=self.view_parking_spaces)
        self.view_button.pack()

        self.query_button = tk.Button(master, text="Query parking record by ticket number", command=self.query_parking_record)
        self.query_button.pack()

        self.quit_button = tk.Button(master, text="Quit", command=self.quit_program)
        self.quit_button.pack()

    def enter_car_park(self):
        registration_window = tk.Toplevel(self.master)
        registration_window.title("Enter Car Park")

        label = tk.Label(registration_window, text="Enter your Car Registration number (Example format: LA07EDC): ")
        label.pack()

        entry = tk.Entry(registration_window)
        entry.pack()

        confirm_button = tk.Button(registration_window, text="Confirm", command=lambda: self.confirm_entry(entry.get()))
        confirm_button.pack()

    def confirm_entry(self, registration_number):
        if self.parking_system.authentication(registration_number):
            if self.parking_system.isCarInParking(registration_number):
                message = "Car with this registration is already parked."
            else:
                parking_space = self.parking_system.createParkingSpace()
                if parking_space:
                    entry_time = DT.now()
                    time_format = entry_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                    ticket_generator = self.parking_system.generateParkingID(registration_number)

                    self.parking_system.car_parking_records.append([registration_number, ticket_generator, f"{parking_space}", entry_time.strftime("%Y-%m-%d %H:%M:%S.%f"), "Parking...", "Parking..."])

                    message = f"Vehicle entered the car park successfully\nVehicle Registration Number: {registration_number}\nParking ID Number: {ticket_generator}\nParking Space ID: {parking_space}\nEntry Time: {time_format}"
                    self.parking_system.writeParkingRecords()
                else:
                    message = "Car park is full"
        else:
            message = "Invalid registration format. Please enter a valid UK-based registration number"

        confirmation_window = tk.Toplevel(self.master)
        confirmation_window.title("Entry Confirmation")

        label = tk.Label(confirmation_window, text=message)
        label.pack()

        ok_button = tk.Button(confirmation_window, text="OK", command=confirmation_window.destroy)
        ok_button.pack()

    def exit_car_park(self):
        exit_window = tk.Toplevel(self.master)
        exit_window.title("Exit Car Park")

        label = tk.Label(exit_window, text="Enter your Car's Registration Number: ")
        label.pack()

        entry = tk.Entry(exit_window)
        entry.pack()

        confirm_button = tk.Button(exit_window, text="Confirm", command=lambda: self.confirm_exit(entry.get()))
        confirm_button.pack()

    def confirm_exit(self, registration_number):
        exit_time = DT.now()
        car_matched = False

        for car_record in self.parking_system.car_parking_records:
            if car_record[0] == registration_number and car_record[4] == "Parking...":
                entry_time_str = car_record[3]
                entry_time = DT.strptime(entry_time_str, "%Y-%m-%d %H:%M:%S.%f")
                total_parking_time = exit_time - entry_time
                parking_fee = self.parking_system.calculateFee(total_parking_time)

                car_record[4] = exit_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                car_record[5] = round(parking_fee, 2)

                message = f"Car has exited the car parking successfully\nExit time: {exit_time}\nParking fee: £{parking_fee}"
                car_matched = True
                break

        if not car_matched:
            message = "Vehicle record not found"

        confirmation_window = tk.Toplevel(self.master)
        confirmation_window.title("Exit Confirmation")

        label = tk.Label(confirmation_window, text=message)
        label.pack()

        ok_button = tk.Button(confirmation_window, text="OK", command=confirmation_window.destroy)
        ok_button.pack()

        self.parking_system.writeParkingRecords()

    def view_parking_spaces(self):
        accessible_spaces = self.parking_system.getAvailableSpaces()
        occupied_spaces = [int(record[2]) for record in self.parking_system.car_parking_records if record[4] == "Parking..."]
        remaining_spaces = len(list(set(accessible_spaces) - set(occupied_spaces)))

        view_window = tk.Toplevel(self.master)
        view_window.title("Available Parking Spaces")

        label = tk.Label(view_window, text=f"Remaining parking spaces: {remaining_spaces}")
        label.pack()

        ok_button = tk.Button(view_window, text="OK", command=view_window.destroy)
        ok_button.pack()

    def query_parking_record(self):
        query_window = tk.Toplevel(self.master)
        query_window.title("Query Parking Record")

        label = tk.Label(query_window, text="Enter your ticket number: ")
        label.pack()

        entry = tk.Entry(query_window)
        entry.pack()

        confirm_button = tk.Button(query_window, text="Confirm", command=lambda: self.confirm_query(entry.get()))
        confirm_button.pack()

    def confirm_query(self, ticket_number):
        found = False
        for record in self.parking_system.car_parking_records:
            if record[1] == ticket_number:
                message = f"Parking record details:\nTicket Number: {record[1]}\nVehicle Registration Number: {record[0]}\nParking space ID: {record[2]}\nEntry Time: {record[3]}\nExit Time: {record[4]}\nParking Fee: £{record[5]}"
                found = True
                break

        if not found:
            message = "Provided ticket number is invalid"

        confirmation_window = tk.Toplevel(self.master)
        confirmation_window.title("Query Result")

        label = tk.Label(confirmation_window, text=message)
        label.pack()

        ok_button = tk.Button(confirmation_window, text="OK", command=confirmation_window.destroy)
        ok_button.pack()

    def quit_program(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    app = CarParkingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
