from .vehicle import Vehicle
from file_handler.file_handler import FileHandler
from exception_handling.Exceptions import CarNotAvailableError
import time

class Car(Vehicle):
    """A car which sets information for a specific vehicle. It is the child class of 'Vehicle'.
    Attributes: car_id, brand, model, seating_capacity, price_per_day, fuel_type, car_type,
    fuel_average,availability
    Methods: display_vehicle_info(), rental_history() """
    def __init__(
            self,
            brand="",
            model="", seating_capacity="",
            price_per_day="", fuel_type="", car_type="",
            fuel_average="",availability=True,
    ):

        super().__init__(brand, model, seating_capacity, price_per_day, availability)
        self.fuel_type = fuel_type
        self.fuel_average = fuel_average
        self.car_type = car_type

#-----------------------------------VEHICLE INSPECTION------------------------------------------------------

    def display_vehicle_info(self):
        print("=" * 30)
        print("ALL AVAILABLE VEHICLES")
        print("=" * 30)
        print()

        file_handler = FileHandler()
        data = file_handler.load_from_file("cars.txt")
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
            print("No Cars Available Right Now")
            self.enter_to_continue()
            print("Returning back to user menu.....\n")
            time.sleep(0.5)
            return

        print("AVAILABLE CARS")
        print("Please type brand and model name from any of the following to view it.")
        self.display_available_cars_names()
        print()

        while True:
            try:
                print("Enter q/Q to exit ")
                brand = input("Brand name (example: Toyota): ").strip()
                if self.quit_choice(brand):
                    return

                model = input("Model name (example: Corolla): ").strip()
                if self.quit_choice(model):
                    return
                if not brand or not model:
                    raise TypeError("Please enter Brand/Model name.")

                car_found = False
                count = 0
                for car in data:
                    if car["brand"].lower() == brand.lower() and car["model"].lower() == model.lower() and car["availability"] == True:
                        count += 1
                        car_found = True
                        brand = car["brand"]
                        model = car["model"]
                        type = car["car_type"]
                        price_per_day = car["price_per_day"]
                        seating_capacity = car["seating_capacity"]
                        fuel_type = car["fuel_type"]
                        fuel_average = car["fuel_average"]
                if not car_found:
                    raise CarNotAvailableError

                print(f"""
{"=" * 25}    
    CAR INFORMATION
{"=" * 25}
{self.bold_italics}Car{self.reset} : {brand} {model}
{self.bold_italics}Car Type: {type}
{"=" * 25}
{self.bold_italics}Seating Capacity{self.reset} : {seating_capacity}
{self.bold_italics}Price/Day{self.reset} : {price_per_day} PKR
{self.bold_italics}Fuel Type{self.reset} : {fuel_type}
{self.bold_italics}Fuel Average{self.reset} : {fuel_average}
{self.bold_italics}Available Cars{self.reset} : {count}
{"=" * 25}""")
                self.enter_to_continue()
                print("Returning back to user menu....")
                time.sleep(0.5)
                return True

            except CarNotAvailableError as e:
                print("Error:",e)
            except TypeError as e:
                print("Error:",e)

    def cars_rental_history(self):
        print("=" * 30)
        print("CARS RENTAL HISTORY")
        print("=" * 30)
        print()
        print("Press q/Q at anytime to quit")
        print()

        file_handler = FileHandler()
        rental_history = file_handler.load_from_file("cars_rental_history.txt")
        if not rental_history:
            print("No cars rental history available.")
            self.enter_to_continue()
            print("Returning back to menu.....\n")
            time.sleep(0.5)
            return

        car_history = []
        self.display_available_cars_names()
        print()
        while True:
            try:
                brand = input("Brand name (example: Toyota): ").strip()
                if self.quit_choice(brand):
                    return
                model = input("Model name (example: Corolla): ").strip()
                if self.quit_choice(model):
                    return
                if not brand or not model:
                    raise ValueError("Please enter Brand/Model name.")

                for car in rental_history:
                    if car["brand"] == brand and car["model"] == model:
                        self.brand = car["brand"]
                        self.model = car["model"]
                        car_history.append(car)

                if not car_history:
                    raise Exception("No rental history found for this car.")

            except ValueError as e:
                print("Error:",e)
            except Exception as e:
                print("Error:",e)
                self.enter_to_continue()
                print("Returning back to user menu....")
                time.sleep(0.5)
                return

            columns = [
                ("S.No.", 5), ("Car ID", 40), ("Rental Date", 15), ("Return Date", 15)
            ]

            print()
            print(f"{self.bold_italics}Car Name:{self.reset} {self.brand} {self.model}")
            header = ""
            for col_name, width in columns:
                header += f"| {self.bold_italics}{col_name:<{width}}{self.reset}"
            print(header + "|")


            for num, rental in enumerate(car_history, start=1):
                row = f"| {num:<{columns[0][1]}}"
                row += f"| {rental['car_id']:<{columns[1][1]}}"
                row += f"| {rental['rental_date']:<{columns[2][1]}}"
                row += f"| {rental['return_date']:<{columns[3][1]}}"
                print(row + "|")

            print()
            self.enter_to_continue()
            print("Returning back to user menu....")
            time.sleep(0.5)
            return





