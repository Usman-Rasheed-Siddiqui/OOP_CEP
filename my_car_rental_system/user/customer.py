from user import User
from rental_management.rental_manager import RentalManager
from datetime import datetime
from file_handler.file_handler import FileHandler
from exception_handling.Exceptions import AlreadyRentedError

class Customer(User):
    def __init__(self, first_name="", last_name="", password="", address="", balance=""):
        super().__init__(first_name, last_name, password)
        self.address = address
        self.balance = balance
        self.file_handler = FileHandler()
        self.name = self.first_name+" "+last_name
        self.all_users = self.file_handler.load_from_file("users.txt")
        self.rented_cars = 0

    def create_an_account(self):

        file_handler = FileHandler()
        all_users = file_handler.load_from_file("users.txt")

        while True:
            try:
                self.first_name = input("Enter your first name: ")
                if not self.first_name:
                    raise ValueError("First Name field are required")
                self.last_name = input("Enter your last name: ")
                if not self.last_name:
                    raise ValueError("Last Name field are required")
                self.password = input("Enter your password: ")
                if not self.password:
                    raise ValueError("Password field are required")
                self.address = input("Enter your address: ")
                if not self.address:
                    raise ValueError("Address field are required")
                self.balance = input("Enter your balance: ")
                if not self.balance.isdigit():
                    raise ValueError("Balance must be an integer")

                self.balance = int(self.balance)
                self.rented_cars = 0
                self.name = self.first_name + " " + self.last_name

                new_user = {
                    "name": self.name,
                    "password": self.password,
                    "address": self.address,
                    "balance": self.balance,
                    "rented_car" : self.rented_cars,
                }

                all_users.append(new_user)
                file_handler.create_file("users", self.name)
                file_handler.save_to_file(all_users,"users.txt")
                print("Your account was successfully created!")
                print("Please login to your account to access it.")
                break

            except ValueError as e:
                print(f"Invalid entry: {e}")

    def display_user_info(self):
        for user in self.all_users:
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


    def check_rent(self, rented_car):
        if rented_car == 1:
            raise AlreadyRentedError("You already have a car rented")

    def renting(self, brand, model, customer):
        file_handler = FileHandler()

        users = file_handler.load_from_file("users.txt")
        try:
            for user in users:
                if user["name"] == customer:
                    self.check_rent(user["rented_car"])

        except AlreadyRentedError as e:
            print(f"Error: {e}")
            return

        safe_name = customer.replace(" ", "_")
        user_rental_history = file_handler.load_from_file(f"users/{safe_name}.txt")

        rental_manager = RentalManager(brand, model)
        car = rental_manager.process_rental(customer)
        if not car:
            return

        rent = {
                "car_id" : car["car_id"],
                "brand" : car["brand"],
                "model" : car["model"],
                "days" : rental_manager.days,
                "rental_date" : rental_manager.rental_date.strftime("%Y-%m-%d"),
                "return_date" : rental_manager.return_date.strftime("%Y-%m-%d"),
                "total_cost" : rental_manager.total_cost,
                }

        for user in users:
            if user["name"] == customer:
                user["rented_car"] = 1

                user_rental_history.append(rent)
                file_handler.save_to_file(users, "users.txt")
                file_handler.save_to_file(user_rental_history, f"users/{safe_name}.txt")
                break

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

user = Customer()
user.renting("Toyota", "Corolla", name)