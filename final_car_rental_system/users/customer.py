from .basic_user import User
#from rental_management.rental_manager import RentalManager
from file_handler.file_handler import FileHandler
from exception_handling.Exceptions import AlreadyRentedError, AccountNotFoundError, WrongPasswordError, PasswordError


class Customer(User):
    def __init__(self, first_name="", last_name="", password="", address="", balance=""):
        super().__init__(first_name, last_name, password)
        self.address = address
        self.balance = balance
        self.file_handler = FileHandler()
        self.all_users = self.file_handler.load_from_file("users.txt")
        self.rented_cars = 0

    def login(self):
        print("=" * 30)
        print("Login")
        print("=" * 30)
        print()
        super().login()
        return self.password_check(self.name, self.password)

    def password_check(self, name, password):
        attempts = 3

        while attempts > 0:
            user_found = False
            password_match = False
            try:
                for user in self.all_users:
                    if user["name"].lower() == name.lower() and user["password"] == password:
                        user_found = True
                        password_match = True
                        break
                if user_found and password_match:
                    print("Username and Password match!")
                    print(f"Welcome onboard! Mr./Mrs. {name.upper()}!")
                    return True

                else:
                    attempts -= 1
                    if attempts > 0:
                        print(f"Password or User name mismatch. You have {attempts} left")
                        name = input("Enter your name: ").strip()
                        password = input("Enter your password: ").strip()

                    if attempts == 0:
                        raise WrongPasswordError

            except WrongPasswordError as e:
                print(f"Error: {e}")
                return False

        return False

    def display_user_info(self):
        pass

    def create_an_account(self):
        print("=" * 30)
        print("Create an Account")
        print("=" * 30)
        print()
        while True:
            try:
                self.first_name = input("Enter your first name: ").strip()
                if not self.first_name:
                    raise ValueError("First Name field is required")
                if len(self.first_name) < 3:
                    raise ValueError("First Name must be at least 3 characters long")
                break
            except ValueError as e:
                print("Invalid Entry:",e)

        while True:
            try:
                self.last_name = input("Enter your last name: ").strip()
                if not self.last_name:
                    raise ValueError("Last Name field is required")
                if len(self.last_name) < 3:
                    raise ValueError("Last Name must be at least 3 characters long")
                break
            except ValueError as e:
                print("Invalid Entry:",e)

        while True:
            try:
                self.password = input("Enter your password: ").strip()
                valid = self.validate_new_password(self.password)
                if valid:
                    break
            except PasswordError as e:
                print("Invalid Entry:",e)

        while True:
            try:
                self.address = input("Enter your address: ").strip()
                if not self.address:
                    raise ValueError("Address field are required")
                break
            except ValueError as e:
                print("Invalid Entry:",e)

        while True:
            try:
                self.balance = input("Enter your balance: ").strip()
                if not self.balance.isdigit():
                    raise ValueError("Balance must be an integer")
                self.balance = int(self.balance)
                if self.balance < 20000:
                    raise ValueError("Balance must be greater than 20000")
                if self.balance > 50000:
                    raise OverflowError("Balance must be less than 50000")
                break

            except ValueError as e:
                print("Invalid Entry:",e)
            except OverflowError as e:
                print("Invalid Entry:",e)

        self.rented_cars = 0
        self.name = self.first_name + " " + self.last_name

        new_user = {
            "name": self.name,
            "password": self.password,
            "address": self.address,
            "balance": self.balance,
            "rented_car" : self.rented_cars,
            }

        self.all_users.append(new_user)
        self.file_handler.create_file("users", self.name)
        self.file_handler.save_to_file(self.all_users,"users.txt")
        print("Your account was successfully created!")
        print("Please login to your account to access it.")
