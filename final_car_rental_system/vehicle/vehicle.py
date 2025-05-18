from abc import ABC, abstractmethod
import uuid
from file_handler.file_handler import FileHandler
import time

class Vehicle(ABC, FileHandler):
    """A class which sets the root for all the cars in the rental system. It is an abstract class.
    Attributes: car_id, brand, model, seating_capacity, price_per_day, availability
    Methods: display_vehicle_info() {abstract method}, display_all_vehicles()"""
    def __init__(self, brand="", model="", seating_capacity="", availability=True, price_per_day=0):
        self.car_id = uuid.uuid4()
        self.brand = brand
        self.model = model
        self.seating_capacity = seating_capacity
        self.price_per_day = price_per_day
        self.availability = availability
        self.bold_italics = '\033[1m\033[3m'
        self.reset = '\033[0m'

    @abstractmethod
    def display_vehicle_info(self):
        """To Display a specific vehicle info"""
        pass

    @staticmethod
    def enter_to_continue():
        while input("Press Enter to continue...") != "":
            print("Please just press Enter without typing anything.")

    def quit_choice(self, choice):
        """Check if user wants to quit (entered 'q' or 'Q')"""
        if choice == "q" or choice == "Q":
            print("Returning back to menu.....\n")
            time.sleep(0.5)
            return True
        return False


    def display_all_vehicles(self):
        """To display info of all vehicles"""
        print("=" * 105)
        print("                                         ALL AVAILABLE VEHICLES")
        print("=" * 105)
        print()

        file_handler = FileHandler()
        cars = file_handler.load_from_file("cars.txt")
        if not cars:
            print("No cars available right now.")
            self.enter_to_continue()
            print("Returning back to menu.....\n")
            time.sleep(0.5)
            return
        true_cars = [car for car in cars if car["availability"]]
        if not true_cars:
            print("No cars available right now.")
            self.enter_to_continue()
            print("Returning back to menu.....\n")
            time.sleep(0.5)
            return

        available_cars = file_handler.load_from_file("available_cars.txt")
        if not available_cars:
            print("No cars available right now.")
            self.enter_to_continue()
            print("Returning back to menu.....\n")
            time.sleep(0.5)
            return

        columns = [
            ("S.No.", 5), ("Brand", 20),  ("Model", 15), ("Seats", 8),
        ("Price/Day (PKR)", 15), ("Type", 10), ("Fuel", 10), ("Average", 10), ("Available", 12)
        ]

        # Counting Availability of a Vehicle
        available_count = {}
        unique_cars = {}
        for car in cars:
            if car["availability"]:
                key = (car["brand"], car["model"])
                if key in available_count:
                    available_count[key] += 1
                else:
                    available_count[key] = 1
                    unique_cars[key] = car


        # Display Header
        header = ""
        for col_name, width in columns:
            header += f"| {self.bold_italics}{col_name:<{width}}{self.reset}"
        print(header + "|")

        # Display the available vehicles
        for num, (key, car) in enumerate(unique_cars.items(), start=1):
                row = f"| {num:>{columns[0][1]}}"
                row += f"| {car["brand"]:<{columns[1][1]}}"
                row += f"| {car['model']:<{columns[2][1]}}"
                row += f"| {car['seating_capacity']:<{columns[3][1]}}"
                row += f"| {car['price_per_day']:<{columns[4][1]}}"
                row += f"| {car['car_type']:<{columns[5][1]}}"
                row += f"| {car['fuel_type']:<{columns[6][1]}}"
                row += f"| {car['fuel_average']:<{columns[7][1]}}"
                row += f"| {available_count[key]:<{columns[8][1]}}"
                print(row + "|")

        self.enter_to_continue()
        print("Returning back to user menu....")
        time.sleep(0.5)


    def display_available_cars_names(self):
        print("AVAILABLE CARS")
        print("Please write brand and model of car from the given list:")
        print()
        file_handler = FileHandler()
        cars = file_handler.load_from_file("cars.txt")

        columns = [
            ("S.No.", 5), ("Brand", 20),  ("Model", 15), ("Price/Day (PKR)", 15), ("Available", 12)
        ]

        # Counting Availability of a Vehicle
        available_count = {}
        unique_cars = {}
        for car in cars:
            if car["availability"]:
                key = (car["brand"], car["model"])
                if key in available_count:
                    available_count[key] += 1
                else:
                    available_count[key] = 1
                    unique_cars[key] = car
        # Display Header
        header = ""
        for col_name, width in columns:
            header += f"| {self.bold_italics}{col_name:<{width}}{self.reset}"
        print(header + "|")

        # Display the available vehicles
        for num, (key, car) in enumerate(unique_cars.items(), start=1):
                row = f"| {num:>{columns[0][1]}}"
                row += f"| {car["brand"]:<{columns[1][1]}}"
                row += f"| {car['model']:<{columns[2][1]}}"
                row += f"| {car['price_per_day']:<{columns[3][1]}}"
                row += f"| {available_count[key]:<{columns[4][1]}}"
                print(row + "|")


