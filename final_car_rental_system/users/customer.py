from .basic_user import User
from rental_management.rental_manager import RentalManager
from file_handler.file_handler import FileHandler
from exception_handling.Exceptions import AlreadyRentedError, AccountNotFoundError, WrongPasswordError, PasswordError
import time

class Customer(User):
    def __init__(self, first_name="", last_name="", password="", address="", balance=""):
        super().__init__(first_name, last_name, password)
        self.address = address
        self.balance = balance
        self.file_handler = FileHandler()
        self.all_users = self.file_handler.load_from_file("users.txt")
        self.rented_cars = 0

    @staticmethod
    def enter_to_continue():
        while input("Press Enter to continue...") != "":
            print("Please just press Enter without typing anything.")

# ------------------------------------------------LOGIN AND SIGN UP-----------------------------------------


    def login(self):
        print("=" * 30)
        print("Login")
        print("=" * 30)
        print()
        if not super().login():
            return False

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
                    print("\nUsername and Password match!")
                    print(f"Welcome onboard! Mr./Mrs. {name.upper()}!\n")
                    time.sleep(0.4)
                    return True

                else:
                    attempts -= 1
                    if attempts > 0:
                        print(f"\nPassword or User name mismatch. You have {attempts} left")
                        name = input("Enter your name: ").strip()
                        password = input("Enter your password: ").strip()

                    if attempts == 0:
                        raise WrongPasswordError

            except WrongPasswordError as e:
                print(f"Error: {e}")
                return False

        return False

    def create_an_account(self):
        print("=" * 30)
        print("Create an Account")
        print("=" * 30)
        print()
        print("Press q/Q at any time to quit\n")
        while True:
            try:
                self.first_name = input("Enter your first name: ").strip()
                if self.quit_choice(self.first_name):
                    return False

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
                if self.quit_choice(self.first_name):
                    return False
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
                if self.quit_choice(self.first_name):
                    return False

                valid = self.validate_new_password(self.password)
                if valid:
                    break
            except PasswordError as e:
                print("Invalid Entry:",e)

        while True:
            try:
                self.address = input("Enter your address: ").strip()
                if self.quit_choice(self.first_name):
                    return False

                if not self.address:
                    raise ValueError("Address field are required")
                break
            except ValueError as e:
                print("Invalid Entry:",e)

        while True:
            try:
                self.balance = input("Enter your balance: ").strip()
                if self.quit_choice(self.first_name):
                    return False

                if not self.balance.isdigit():
                    raise ValueError("Balance must be an integer")
                self.balance = int(self.balance)
                if self.balance < 20000:
                    raise ValueError("Balance must be greater than 20000 PKR")
                if self.balance > 50000:
                    raise OverflowError("Balance can be at most 50000 PKR")
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
        return True

# -----------------------------------------RENTING AND RETURNING PROCESS-----------------------------------

    def check_rent(self, rented_car):
        if rented_car == 1:
            raise AlreadyRentedError("You already have a car rented\n")

    # RENTING
    def renting(self):
        print("="*30)
        print("RENTING")
        print("="*30)
        print()
        print("Press q/Q at anytime to quit.")
        print()
        users = self.all_users
        user_found = False
        customer = self.name
        try:
            for user in users:
                if user["name"].lower() == customer.lower():
                    user_found = True
                    self.name = user["name"]
                    self.check_rent(user["rented_car"])

            if not user_found:
                raise AccountNotFoundError

        except AlreadyRentedError as e:
            print(f"Error: {e}")
            return False
        except AccountNotFoundError as e:
            print(f"Error: {e}")
            return False

        brand = input("Enter brand you want to rent: ").strip()
        if self.quit_choice(brand):
            return False
        model = input("Enter model you want to rent: ").strip()
        if self.quit_choice(model):
            return False


        safe_name = customer.replace(" ", "_")
        user_rental_history = self.file_handler.load_from_file(f"users/{safe_name}.txt")

        rental_manager = RentalManager(brand, model)
        car = rental_manager.process_rental(customer)
        if not car:
            return False

        rent = {
                "car_id" : car["car_id"],
                "brand" : car["brand"],
                "model" : car["model"],
                "days" : rental_manager.days,
                "rental_date" : rental_manager.rental_date.strftime("%Y-%m-%d"),
                "return_date" : rental_manager.return_date.strftime("%Y-%m-%d"),
                "total_cost" : rental_manager.total_cost,
                }
        try:
            for user in users:
                if user["name"] == customer:
                    if user["balance"] < rental_manager.total_cost:
                       raise Exception("You don't have enough money to rent this car. Please update your balance and try again.")

                    user["balance"] -= rental_manager.total_cost
                    user["rented_car"] = 1

                    user_rental_history.append(rent)
                    self.file_handler.save_to_file(users, "users.txt")
                    self.file_handler.save_to_file(user_rental_history, f"users/{safe_name}.txt")
                    time.sleep(0.5)
                    print("Preparing your car....")
                    time.sleep(0.5)
                    print("Getting it ready.....")
                    time.sleep(0.5)
                    print("\nYour Car was rented successfully!")
                    rental_manager.print_receipt(self.name)
                    self.enter_to_continue()
                    print("Returning back to user menu.....")
                    time.sleep(0.5)

            return True

        except Exception as e:
            print(f"Error: {e}")
            return False

    # RETURNING
    def returning(self):
        print("=" * 30)
        print("RETURNING")
        print("=" * 30)
        print()
        car_id = input("Enter car id: ")
        self.quit_choice(car_id)

        rental_manager = RentalManager()
        car = rental_manager.process_return(car_id, self.name)
        if not car:
            return False

        users = self.all_users
        for user in users:
            if user["name"] == self.name:
                user["rented_car"] = 0

        print("Preparing to take your car...")
        time.sleep(0.5)
        print("Inspecting the car for a smooth return process...")
        time.sleep(0.5)
        print("Almost done!...")
        time.sleep(0.5)
        print("Your car was returned successfully!")
        self.enter_to_continue()
        print("Returning back to user menu.....")
        time.sleep(0.5)
        self.file_handler.save_to_file(users, f"users.txt")
        return True

# ----------------------------------------------USER INSPECTION--------------------------------------------
    def display_user_info(self):
        for user in self.all_users:
            try:
                if user["name"].lower() == self.name.lower():
                    print (f"""
{"="*30}
      USER INFORMATION
{"="*30}
Name : {user["name"]}
Address : {user["address"]}
Balance : {user["balance"]}
{"="*30}
""")
                    self.enter_to_continue()
            except ValueError:
                print("An Error occurred. Please try again")
                print("Returning back to user menu.....")
                time.sleep(0.5)
                return

#------------------------------------------------BALANCE UPDATE--------------------------------------------

    def update_balance(self):

        print("=" * 30)
        print("BALANCE UPDATE")
        print("=" * 30)
        print("Press q/Q at any time to quit")
        print()
        users = self.all_users
        while True:
            try:
                for user in users:
                    if user["name"].lower() == self.name.lower():
                        balance = input("Enter your balance to be updated: ")

                        if self.quit_choice(self.first_name):
                            return False

                        if not balance.isdigit():
                            raise ValueError("Balance must be an integer")

                        balance = int(balance)

                        if balance <= 0:
                            raise ValueError("Balance must be greater than 0")

                        if user["balance"] + balance < 20000:
                            raise ValueError("Balance must be greater than 20000 PKR")

                        if user["balance"] + balance > 50000:
                            raise OverflowError("Balance can be at most 50000 PKR")

                        user["balance"] += balance
                        self.file_handler.save_to_file(users, "users.txt")
                        print("Balance updated successfully!")
                        time.sleep(0.5)
                        print("Returning back to user menu.....")
                        time.sleep(0.5)
                        return

            except ValueError as e:
                print(f"Error: {e}")
            except OverflowError as e:
                print(f"Error: {e}")





