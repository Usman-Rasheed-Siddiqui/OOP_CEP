from user import User
from file_handler.file_handler import FileHandler
from exception_handling.Exceptions import WrongPasswordError
import uuid


class Admin(User):
    def __init__(self, password=""):
        super().__init__(password)
        self.file_handler = FileHandler()

    def login(self):
        super().login()
        self.check_admin_password(self.name.strip(), self.password)

    def check_admin_password(self, name, password, dashboard=None, menu=None):
        attempts = 3

        while attempts > 0:
            try:
                    if name.lower() == "admin":
                        if password == "admin@123":
                            print("Password match!")
                            print(f"Welcome onboard! Mr.{name}")
                            return dashboard
                        else:
                            attempts -= 1
                            print(f"Password or name mismatch. You have {attempts} left")
                            if attempts == 0:
                                raise WrongPasswordError
                            print("Try again!")
                            name = input("Enter name: ")
                            password = input("Enter password: ")

            except WrongPasswordError as e:
                print(f"Error: {e}")

        return menu

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

    def add_a_new_car(self,brand, model, seating_capacity, price_per_day, fuel_type, car_type,
            fuel_average,availability=True):

        available_cars = self.file_handler.load_from_file("available_cars.txt")
        new_car = {
            "car_id": uuid.uuid4(),
            "brand": brand,
            "model": model,
            "seating_capacity": seating_capacity,
            "price_per_day": price_per_day,
            "car_type": car_type,
            "fuel_type": fuel_type,
            "fuel_average": fuel_average,
            "availability": availability,
        }
        available_cars.append(new_car)
        self.file_handler.save_to_file(available_cars,"available_cars.txt")
        return new_car

    def  remove_car(self, brand, model):
        available_cars = self.file_handler.load_from_file("available_cars.txt")
        for car in available_cars:
            if car["brand"] == brand and car["model"] == model:
                available_cars.remove(car)

        self.file_handler.save_to_file(available_cars,"available_cars.txt")

    def access_feedbacks(self):
        feedbacks = self.file_handler.load_from_file("feedbacks.txt")
        for feedback in feedbacks:
            print(f"{feedback["Name"]} : {feedback['Feedback']}")

