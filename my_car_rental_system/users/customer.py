from .basic_user import User
from rental_management.rental_manager import RentalManager
from file_handler.file_handler import FileHandler
from exception_handling.Exceptions import AlreadyRentedError, AccountNotFoundError, WrongPasswordError


class Customer(User):
    def __init__(self, first_name="", last_name="", password="", address="", balance=""):
        super().__init__(first_name, last_name, password)
        self.address = address
        self.balance = balance
        self.file_handler = FileHandler()
        self.all_users = self.file_handler.load_from_file("users.txt")
        self.rented_cars = 0

    def login(self):
        super().login()
        return self.password_check(self.name.strip(), self.password)

    def password_check(self, name, password):
        attempts = 3
        file_handler = FileHandler()
        users = file_handler.load_from_file("users.txt")

        while attempts > 0:
            user_found = False
            password_match = False
            try:
                for user in users:
                    if user["name"].lower() == name.lower():
                        user_found = True
                    if user["password"] == password:
                        password_match = True

                if user_found and password_match:
                    print("Username and Password match!")
                    print(f"Welcome onboard! Mr./Mrs. {name}")
                    return True
                else:
                    attempts -= 1
                    if attempts > 0:
                        print(f"Password or User name mismatch. You have {attempts} left")
                        name = input("Enter your name: ")
                        password = input("Enter your password: ")

                    if attempts == 0:
                        raise WrongPasswordError

            except WrongPasswordError as e:
                print(f"Error: {e}")

        return False

    def create_an_account(self):

        file_handler = FileHandler()
        all_users = file_handler.load_from_file("users.txt")

        while True:
            try:
                self.first_name = input("Enter your first name: ").strip()
                if not self.first_name:
                    raise ValueError("First Name field are required")
                break
            except ValueError as e:
                print("Invalid Entry:",e)

        while True:
            try:
                self.last_name = input("Enter your last name: ").strip()
                if not self.last_name:
                    raise ValueError("Last Name field are required")
                break
            except ValueError as e:
                print("Invalid Entry:",e)

        while True:
            try:
                self.password = input("Enter your password: ")
                if not self.password:
                    raise ValueError("Password field are required")
                break
            except ValueError as e:
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
                break
            except ValueError as e:
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

        all_users.append(new_user)
        file_handler.create_file("users", self.name)
        file_handler.save_to_file(all_users,"users.txt")
        print("Your account was successfully created!")
        print("Please login to your account to access it.")


    def check_rent(self, rented_car):
        if rented_car == 1:
            raise AlreadyRentedError("You already have a car rented")


    def renting(self):
        brand = input("Enter brand you want to rent: ")
        model = input("Enter model you want to rent: ")
        customer = self.name

        file_handler = FileHandler()
        users = file_handler.load_from_file("users.txt")
        user_found = False

        try:
            for user in users:
                if user["name"] == customer:
                    user_found = True
                    self.check_rent(user["rented_car"])
            if not user_found:
                raise AccountNotFoundError

        except AlreadyRentedError as e:
            print(f"Error: {e}")
            return
        except AccountNotFoundError as e:
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
        try:
            for user in users:
                if user["name"] == customer:
                    if user["balance"] < rental_manager.total_cost:
                       raise Exception("You don't have enough money to rent this car. Please update your balance and try again.")

                    user["balance"] -= rental_manager.total_cost
                    user["rented_car"] = 1

                    user_rental_history.append(rent)
                    file_handler.save_to_file(users, "users.txt")
                    file_handler.save_to_file(user_rental_history, f"users/{safe_name}.txt")
                    rental_manager.print_receipt(self.name)
                    break
        except Exception as e:
            print(f"Error: {e}")


    def returning(self):

        car_id = input("Enter car id: ")
        rental_manager = RentalManager()
        car = rental_manager.process_return(car_id, self.name)
        if not car:
            return
        file_handler = FileHandler()
        users = file_handler.load_from_file("users.txt")

        for user in users:
            if user["name"] == self.name:
                user["rented_car"] = 0

        file_handler.save_to_file(users, f"users.txt")


    def write_feedback(self):
        feedbacks = self.file_handler.load_from_file("feedbacks.txt")
        print("We love to hear from you. Write your valuable feedback here please:")
        while True:
            try:
                feedback = input("Feedback: ")
                if not feedback:
                    raise ValueError("Feedback cannot be empty")
                break
            except ValueError as e:
                print(f"Error: {e}")

        feedback = {
            "Name" : self.name,
            "Feedback" : feedback,
        }
        if feedbacks:
            print("Thank you for your feedback!")
        feedbacks.append(feedback)
        self.file_handler.save_to_file(feedbacks, "feedbacks.txt")



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
            except ValueError:
                print("An Error occurred. Please try again")

