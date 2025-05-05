from file_handler.file_handler import FileHandler
from rental_management.rental_manager import RentalManager

class Testing:
    def __init__(self, first_name="", last_name="", password="", address="", balance=0):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.address = address
        self.balance = balance
        self.rented_cars = 0
        self.name = self.first_name + " " + self.last_name

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

T1 = Testing()
T1.create_an_account()


