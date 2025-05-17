from .basic_user import User
from file_handler.file_handler import FileHandler
from exception_handling.Exceptions import WrongPasswordError, PasswordError, CarNotFoundError
from vehicle.car import Car
import uuid
import time

class Admin(User):
    def __init__(self, password="",brand="", model="", seating_capacity="", price_per_day=0, fuel_type="", car_type="",
            fuel_average="",availability=True):
        super().__init__(password)
        self.file_handler = FileHandler()
        self.admin_info = self.file_handler.load_from_file("admin_info.txt")
        self.car = Car(brand, model, seating_capacity, price_per_day, fuel_type, car_type,fuel_average, availability)
        self.cars = self.file_handler.load_from_file("cars.txt")
        self.available_cars = self.file_handler.load_from_file("available_cars.txt")

    def login(self):
        print("=" * 30)
        print("LOGIN ADMIN")
        print("=" * 30)
        print()
        if not super().login():
            return False
        if self.check_admin_password():
            return True

    def update_info(self, member = None):
        self.admin_info = self.file_handler.load_from_file("admin_info.txt")
        while True:
            try:
                for admin in self.admin_info:
                    super().update_info(admin)
                    admin["password"] = self.password
                self.file_handler.save_to_file(self.admin_info, "admin_info.txt")
                print("Information Updated successfully")
                time.sleep(0.5)
                print("Returning back to admin menu....")
                time.sleep(0.5)
                break

            except PasswordError as e:
                print("Error:", e)

    def check_admin_password(self):
        self.admin_info = self.file_handler.load_from_file("admin_info.txt")
        attempts = 3
        while attempts > 0:
            try:
                for admin in self.admin_info:
                    if self.email.lower() == admin["email"].lower():
                        if self.password == admin["password"]:
                            self.name = admin["name"]
                            print("Password match!")
                            print(f"Welcome onboard! Mr.{self.name}")
                            return True
                        else:
                            attempts -= 1
                            print(f"Password or name mismatch. You have {attempts} left")
                            if attempts == 0:
                                raise WrongPasswordError
                            print("Try again!")
                            self.email = input("Enter your email: ")
                            self.password = input("Enter your password: ")

            except WrongPasswordError as e:
                print(f"Error: {e}")

        return False

    def add_new_car_fleet(self,availability=True):
        print("=" * 30)
        print("ADD NEW FLEET")
        print("=" * 30)
        print("Press q/Q at anytime to quit the process")
        print()
        self.cars = self.file_handler.load_from_file("cars.txt")
        self.available_cars = self.file_handler.load_from_file("available_cars.txt")

        while True:
            try:
                no_of_cars = input("Enter the number of cars to be added: ").strip()
                if self.quit_choice(no_of_cars):
                    return
                if not no_of_cars.isdigit():
                    raise TypeError("Number of cars must be an integer")
                if not no_of_cars:
                    raise ValueError("Number of cars is required")
                no_of_cars = int(no_of_cars)
                break
            except TypeError as e:
                print("Error:",e)
            except ValueError as e:
                print("Error:",e)

        while True:
            try:
                self.car.brand = input("Enter brand name: ").strip()
                if self.quit_choice(self.car.brand):
                    return
                if not self.car.brand:
                    raise ValueError("Brand name is required")
                break
            except ValueError as e:
                print("Error:",e)

        while True:
            try:
                self.car.model = input("Enter model name: ").strip()
                if self.quit_choice(self.car.model):
                    return
                if not self.car.model:
                    raise ValueError("Model name is required")
                break
            except ValueError as e:
                print("Error:",e)

        while True:
            try:
                self.car.seating_capacity = input("Enter seating capacity: ").strip()
                if self.quit_choice(self.car.seating_capacity):
                    return
                if not self.car.seating_capacity.isdigit():
                    raise TypeError("Number of seating capacity must be an integer")
                if not self.car.seating_capacity:
                    raise ValueError("Seating capacity is required")
                break
            except TypeError as e:
                print("Error:",e)

            except ValueError as e:
                print("Error:",e)

        while True:
            try:
                self.car.price_per_day = input("Enter price per day: ").strip()
                if self.quit_choice(self.car.price_per_day):
                    return
                if not self.car.price_per_day:
                    raise ValueError("Price per day is required")
                if not self.car.price_per_day.isdigit():
                    raise TypeError("Price per day must be a number")
                self.car.price_per_day = int(self.car.price_per_day)
                break
            except TypeError as e:
                print("Error:",e)
            except ValueError as e:
                print("Error:",e)

        while True:
            try:
                self.car.fuel_type = input("Enter fuel type: ").strip()
                if self.quit_choice(self.car.fuel_type):
                    return
                if not self.car.fuel_type:
                    raise ValueError("Fuel type is required")
                break
            except ValueError as e:
                print("Error:",e)

        while True:
            try:
                self.car.car_type = input("Enter car type: ").strip()
                if self.quit_choice(self.car.car_type):
                    return
                if not self.car.car_type:
                    raise ValueError("Car type is required")
                break
            except ValueError as e:
                print("Error:",e)

        while True:
            try:
                self.car.fuel_average = input("Enter fuel average: ").strip()
                if self.quit_choice(self.car.fuel_average):
                    return
                if not self.car.fuel_average.isdigit():
                    raise TypeError("Fuel average must be a number")
                if not self.car.fuel_average:
                    raise ValueError("Fuel average is required")
                self.car.fuel_average = int(self.car.fuel_average)
                break
            except TypeError as e:
                print("Error:",e)
            except ValueError as e:
                print("Error:",e)

        self.car.availability = availability
        cars = self.cars
        available_cars = self.available_cars

        for car in range(no_of_cars):
            car_id = str(uuid.uuid4())
            new_car = {
                "car_id": car_id,
                "brand": self.car.brand,
                "model": self.car.model,
                "seating_capacity": self.car.seating_capacity,
                "price_per_day": self.car.price_per_day,
                "car_type": self.car.car_type,
                "fuel_type": self.car.fuel_type,
                "fuel_average": self.car.fuel_average,
                "availability": self.car.availability,
                }
            new_available_car = {
                'car_id': car_id,
                'customer': None,
                'brand': self.car.brand,
                'model': self.car.model,
                'rental_data': None,
                'return_date': None,
                'total_days': 0,
                'total_cost': 0
            }

            cars.append(new_car)
            available_cars.append(new_available_car)

        self.file_handler.save_to_file(cars,"cars.txt")
        self.file_handler.save_to_file(available_cars,"available_cars.txt")

        print("Saving details for new car....")
        time.sleep(0.5)
        print("Getting everything ready....")
        time.sleep(0.5)
        print("New car was added successfully....")
        time.sleep(0.5)
        time.sleep(0.5)
        print("Returning back to admin menu....")

    def display_user_info(self):
        users = self.file_handler.load_from_file("users.txt")
        name = input("Enter username to check his details: ")
        safe_name = name.replace(" ", "_")
        one_user = self.file_handler.load_from_file(f"users/{safe_name}.txt")
        while True:
            try:
                user_found = False
                for user in users:
                    if user["name"] == name:
                        user_found = True
                        print(f"""
            {"=" * 30}
                  USER BASIC INFORMATION
            {"=" * 30}
            Name : {user["name"]}
            Address : {user["address"]}
            Balance : {user["balance"]}
            {"=" * 30}
            """)

                    print(f"""
            {"=" * 30}
                  USER RENTAL INFORMATION
            {"=" * 30}""")
                    for car in one_user:
                        for key, value in car.items():
                            print(f"{key} | {value}")
                    print({"=" * 30})
                    break

                if not user_found:
                    raise ValueError("User with this name does not exist")

            except ValueError as e:
                print("Error:",e)
            except TypeError as e:
                print("Error:",e)

            return

    def remove_car_fleet(self):
        print("=" * 30)
        print("REMOVE CAR FLEET")
        print("=" * 30)
        print("Press q/Q at anytime to quit the process")
        print()
        self.cars = self.file_handler.load_from_file("cars.txt")
        self.available_cars = self.file_handler.load_from_file("available_cars.txt")

        while True:
            try:
                self.car.brand = input("Enter brand name: ").strip()
                if self.quit_choice(self.car.brand):
                    return
                if not self.car.brand:
                    raise ValueError("Brand name is required")
                break
            except ValueError as e:
                print("Error:", e)
        while True:
            try:
                self.car.model = input("Enter model name: ").strip()
                if self.quit_choice(self.car.model):
                    return
                if not self.car.model:
                    raise ValueError("Model name is required")
                break
            except ValueError as e:
                print("Error:", e)

                return

        available_cars = self.available_cars
        cars = self.cars
        available_cars = [
            car for car in available_cars
            if not (car["brand"].lower() == self.car.brand.lower()
                    and car["model"].lower() == self.car.model.lower())
        ]

        cars = [
            car for car in cars
            if not (car["brand"].lower() == self.car.brand.lower()
                    and car["model"].lower() == self.car.model.lower()
                    and car["availability"])
        ]


        self.file_handler.save_to_file(available_cars,"available_cars.txt")
        self.file_handler.save_to_file(cars,"cars.txt")
        print("Please Note: Only those cars of the fleets will be removed")
        print("if they are not rented. The rented ones can be removed later when returned")
        time.sleep(0.5)
        print("Cars successfully removed....")
        self.enter_to_continue()
        print("Returning back to admin menu....")
        time.sleep(0.5)

    def access_feedbacks(self):
        feedbacks = self.file_handler.load_from_file("feedbacks.txt")
        for feedback in feedbacks:
            print(f"{feedback["Name"]} : {feedback['Feedback']}")

