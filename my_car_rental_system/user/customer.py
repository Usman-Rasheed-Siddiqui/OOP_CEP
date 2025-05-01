from user import User
from rental_management.rental_manager import RentalManager
from datetime import datetime
from file_handler.file_handler import FileHandler
from vehicle.car import Car

class Customer(User):
    def __init__(self, first_name="", last_name="", password="", address="", balance=""):
        super().__init__(first_name, last_name, password)
        self.address = address
        self.balance = balance
        self.file_handler = FileHandler()
        self.user_rental_history = self.file_handler.load_from_file("users.txt")
        self.rented_cars = 0

    def check_rent(self):
        if self.rented_cars == 1:
            print("You cannot rent a car. You have already a car rented")

    def create_an_account(self, first_name, last_name, password, address, balance):

        self.first_name = input("Enter your first name: ")
        self.last_name = input("Enter your last name: ")
        self.password = input("Enter your password: ")
        self.address = input("Enter your address: ")
        self.balance = int(input("Enter your balance: "))
        self.rented_cars = 0

        new_user = {
            "name": {self.name},
            "password": {self.password},
            "address": {self.address},
            "balance": self.balance,
            "rented Car" : {self.rented_cars},
            "recent Rent": None,
        }
        self.user_rental_history.append(new_user)
        self.file_handler.save_to_file(self.user_rental_history,"users.txt")
        return new_user

    def display_user_info(self):
        data = self.user_rental_history

        return f"""
{"="*30}
USER INFORMATION
{"="*30}
Name : {self.name}
Address : {self.address}
Balance : {self.balance}
{"="*30}
"""

    def save_user_info(self):
        car = Car(None, None, None, None, None, None, None)

        renting_info = {
            "Name" : {self.name},
            "Password": {self.password},
            "Address" : {self.address},
            "Balance" : {self.balance},
            "Rented Cars" : {self.rented_cars},
            "Recent Rent" : {car.car_id}
        }

        for user in self.user_rental_history:
            if user["Name"] == self.name:
                self.user_rental_history.remove(user)
                self.user_rental_history.append(renting_info)

    def renting(self, brand, model, days):
        car = Car(brand, model, None, None, None, None, None)
        rental_manager = RentalManager(days, car, customer=self)
        rental_manager.process_rental()
        renting = {
            "car_id" : car.car_id,
            "brand" : car.brand,
            "model" : car.model,
            "days" : rental_manager.days,
            "rental_date" : rental_manager.rental_date,
            "cost" : rental_manager.total_cost,
        }
        self.rented_cars += 1
        self.user_rental_history.append(renting)

    def returning(self,customer,car_id, days = None, car = None, brand = None, model = None):

        rental_manager = RentalManager(days, car, customer=self)
        rental_manager.process_return()
        car = Car(brand, model, None, None, None, None, None)

        for user in self.user_rental_history:
            if user["name"] == customer:
                for rent in user:
                    if rent["car_id"] == car.car_id == car_id:
                        rent["return_date"] = datetime.now()
                    else:
                        raise Exception("No car rented with this ID")


    def write_feedback(self, feedback):
        feedbacks = self.file_handler.load_from_file("feedbacks.txt")
        feedback = {
            "Name" : {self.name},
            "Feedback" : feedback,
        }
        feedbacks.append(feedback)
        self.file_handler.save_to_file(feedbacks, "feedbacks.txt")

    def password_check(self, name, password, page):
        for user in self.user_rental_history:
            while range == 3:
                if user["Name"].lower() == name.lower() and user["password"] == password:
                    print("Password match")
                    return page
                else:
                    raise Exception("Password mismatch. Try again (3 attempts total)")
        return None
