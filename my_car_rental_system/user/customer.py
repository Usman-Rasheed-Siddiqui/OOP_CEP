from user import User
from rental_management.rental_manager import RentalManager
from datetime import datetime
from file_handler.file_handler import FileHandler

class Customer(User):
    def __init__(self, first_name="", last_name="", password="", address="", balance=""):
        super().__init__(first_name, last_name, password)
        self.address = address
        self.balance = balance
        self.file_handler = FileHandler()
        self.name = self.first_name+" "+last_name
        self.user_rental_history = self.file_handler.load_from_file("users.txt")
        self.rented_cars = 0

    def check_rent(self):
        if self.rented_cars == 1:
            print("You cannot rent a car. You have already a car rented")

    def create_an_account(self):

        self.first_name = input("Enter your first name: ")
        self.last_name = input("Enter your last name: ")
        self.password = input("Enter your password: ")
        self.address = input("Enter your address: ")
        self.balance = int(input("Enter your balance: "))
        self.rented_cars = 0
        self.name = self.first_name+" "+self.last_name

        new_user = {
            "name": self.name,
            "password": self.password,
            "address": self.address,
            "balance": self.balance,
            "rented car" : self.rented_cars,
        }

        self.user_rental_history.append(new_user)
        self.file_handler.save_to_file(self.user_rental_history,"users.txt")
        print("Your account was successfully created!")
        return new_user

    def display_user_info(self):
        data = self.user_rental_history
        for user in data:
            try:
                if user["name"] == self.name:
                    print (f"""
{"="*30}
USER INFORMATION
{"="*30}
Name : {user["name"]}
Address : {user["address"]}
Balance : {user["balance"]}
{"="*30}
""")
            except:
                raise ValueError("An Error occurred. Please try again")

    def renting(self, brand, model, customer):
        cars = self.file_handler.load_from_file("cars.txt")
        for car in cars:
            try:
                if car["brand"] == brand and car["model"] == model:
                    rental_manager = RentalManager(brand, model)
                    rental_manager.process_rental(customer)
                    renting = {
            "car_id" : car["car_id"],
            "brand" : brand,
            "model" : model,
            "days" : rental_manager.days,
            "rental_date" : rental_manager.rental_date,
            "cost" : rental_manager.total_cost,
                    }
                    self.rented_cars = 1
                    self.user_rental_history.append(renting)
                    break

            except ValueError:
                print("No such car with this brand and model found")

    def returning(self, car_id):

        rental_manager = RentalManager()
        rental_manager.process_return(car_id, self.name)

        for user in self.user_rental_history:
            if user["name"] == self.name:
                for rent in user:
                    if rent["car_id"]  == car_id:
                        rent["return_date"] = datetime.now()
                    else:
                        raise Exception("No car rented with this ID")

    def save_user_info(self, car_id):

        user_info = {
            "name" : {self.name},
            "password": {self.password},
            "address" : {self.address},
            "balance" : {self.balance},
            "rented car" : {self.rented_cars},
            "recent rent" : {car_id}
        }

        for user in self.user_rental_history:
            if user["name"] == self.name:
                self.user_rental_history.remove(user)
                self.user_rental_history.append(user_info)


    def write_feedback(self, feedback):
        feedbacks = self.file_handler.load_from_file("feedbacks.txt")
        feedback = {
            "Name" : {self.name},
            "Feedback" : feedback,
        }
        feedbacks.append(feedback)
        self.file_handler.save_to_file(feedbacks, "feedbacks.txt")

    def password_check(self, name, password, page, menu):
        attempts = 3
        for user in self.user_rental_history:
            while attempts > 0:
                if user["name"].lower() == name.lower() and user["password"] == password:
                    print("Password match!")
                    print(f"Welcome onboard! Mr./Mrs. {name}")
                    return page
                else:
                    attempts -= 1
                    print(f"Password or User name mismatch. You have {attempts} left")
                    if attempts == 0:
                        raise Exception("Password or User name mismatch. No attempts left")

                    print("Try again!")
                    name = input("Enter your name: ")
                    password = input("Enter your password: ")

        return menu

name = input("Enter your name: ")
password = input("Enter your password: ")

user = Customer()
user.password_check(name, password, "", "")
user.renting("Toyota", "Corolla", name)
user.save_user_info("2c026418-6111-4d4a-a91b-dffd2626ec7b")