from .basic_user import User
from vehicle.car import Car
from rental_management.rental_manager import RentalManager
from file_handler.file_handler import FileHandler
from exception_handling.Exceptions import AlreadyRentedError, AccountNotFoundError, WrongPasswordError, PasswordError, CustomerNoRentsError
import time

class Customer(User):
    def __init__(self, brand="",model="", first_name="", last_name="", email="",password="", address="", balance=""):
        super().__init__(first_name, last_name, email, password)
        self.car = Car(brand, model)
        self.address = address
        self.balance = balance
        self.file_handler = FileHandler()
        self.all_users = self.file_handler.load_from_file("users.txt")
        self.cars_rented = self.file_handler.load_from_file("rented_cars.txt")
        self.rented_cars = 0
        self.name = ""
        self.safe_name = ""
        self.safe_email = ""

# ------------------------------------------------LOGIN AND SIGN UP-----------------------------------------

    def login(self):
        print("=" * 30)
        print("Login")
        print("=" * 30)
        print()
        if not super().login():
            return False

        return self.password_check(self.email, self.password)

    def password_check(self, email, password):
        attempts = 3
        self.all_users = self.file_handler.load_from_file("users.txt")
        self.cars_rented = self.file_handler.load_from_file("rented_cars.txt")

        while attempts > 0:
            user_found = False
            password_match = False
            try:
                for user in self.all_users:
                    if user["email"].lower() == email.lower() and user["password"] == password:
                        user_found = True
                        password_match = True
                        self.name = user["name"]
                        break
                if user_found and password_match:
                    print("\nUsername and Password match!")
                    print(f"Welcome onboard! Mr./Mrs. {self.name.upper()}!\n")
                    time.sleep(0.4)
                    return True

                else:
                    attempts -= 1
                    if attempts > 0:
                        print(f"\nPassword or User name mismatch. You have {attempts} left")
                        email = input("Enter your email: ").strip()
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

        self.all_users = self.file_handler.load_from_file("users.txt")
        self.cars_rented = self.file_handler.load_from_file("rented_cars.txt")
        while True:
            try:
                self.first_name = input("Enter your first name: ").strip()
                if self.quit_choice(self.first_name):
                    return

                if not self.first_name:
                    raise ValueError("First Name field is required")

                if len(self.first_name) < 3:
                    raise ValueError("First Name must be at least 3 characters long")

                if len(self.first_name) > 20:
                    raise ValueError("Last Name must be at most 20 characters long")
                break
            except ValueError as e:
                print("Invalid Entry:",e)

        while True:
            try:
                self.last_name = input("Enter your last name: ").strip()
                if self.quit_choice(self.first_name):
                    return
                if not self.last_name:
                    raise ValueError("Last Name field is required")
                if len(self.last_name) < 3:
                    raise ValueError("Last Name must be at least 3 characters long")
                if len(self.last_name) > 20:
                    raise ValueError("Last Name must be at most 20 characters long")
                break
            except ValueError as e:
                print("Invalid Entry:",e)

        while True:
            try:
                self.email = input("Enter your email: ").strip().lower()
                if self.quit_choice(self.first_name):
                    return
                if not self.email:
                    raise ValueError("Email field is required")

                self.validate_email(self.email)

                for user in self.all_users:
                    if user["email"] == self.email:
                        raise ValueError("Email already registered")
                break

            except ValueError as e:
                print("Error:",e)
        while True:
            try:
                self.password = input("Enter your password: ").strip()
                if self.quit_choice(self.first_name):
                    return
                for user in self.all_users:
                    if user["password"] == self.password:
                        raise PasswordError("Password already exists")

                valid = self.validate_new_password(self.password)
                if valid:
                    break
            except PasswordError as e:
                print("Error:",e)

        while True:
            try:
                self.address = input("Enter your address: ").strip()
                if self.quit_choice(self.first_name):
                    return

                if not self.address:
                    raise ValueError("Address field are required")

                if len(self.address) > 50:
                    raise OverflowError("Address cannot be longer than 50 characters")

                if self.address.isdigit():
                    raise Exception("Address can't be just an integer")

                break
            except ValueError as e:
                print("Invalid Entry:",e)

            except OverflowError as e:
                print("Error:",e)

        while True:
            try:
                self.balance = input("Enter your balance: ").strip()
                if self.quit_choice(self.first_name):
                    return

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
            "email": self.email,
            "password": self.password,
            "address": self.address,
            "balance": self.balance,
            "rented_car" : self.rented_cars,
            }

        self.all_users.append(new_user)
        self.file_handler.create_file("users", self.email)
        self.file_handler.save_to_file(self.all_users,"users.txt")
        print("Your account was successfully created!")
        print("Please login to your account to access it.")
        return True

# -----------------------------------------RENTING AND RETURNING PROCESS-----------------------------------

    # CHECKING RENTS
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

        self.all_users = self.file_handler.load_from_file("users.txt")
        self.cars_rented = self.file_handler.load_from_file("rented_cars.txt")
        rental_history = self.file_handler.load_from_file("cars_rental_history.txt")

        users = self.all_users
        user_found = False
        customer = self.email
        try:
            for user in users:
                if user["email"].lower() == customer.lower():
                    user_found = True
                    self.email = user["email"]
                    customer = user["email"]
                    self.check_rent(user["rented_car"])

            if not user_found:
                raise AccountNotFoundError

        except AlreadyRentedError as e:
            print(f"Error: {e}")
            self.enter_to_continue()
            return
        
        except AccountNotFoundError as e:
            print(f"Error: {e}")
            return False

        brand = input("Enter brand you want to rent: ").strip()
        if self.quit_choice(brand):
            return
        model = input("Enter model you want to rent: ").strip()
        if self.quit_choice(model):
            return

        self.safe_email = customer.replace("@", "_at_").replace(".", "_dot_")
        user_rental_history = self.file_handler.load_from_file(f"users/{self.safe_email}.txt")

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

        for user in users:
            if user["email"].lower() == customer.lower():
                user["balance"] -= rental_manager.total_cost
                user["rented_car"] = 1

                user_rental_history.append(rent)
                rental_history.append(rent)

                self.file_handler.save_to_file(users, "users.txt")
                self.file_handler.save_to_file(user_rental_history, f"users/{self.safe_email}.txt")
                self.file_handler.save_to_file(rental_history, "cars_rental_history.txt")

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


    # RETURNING
    def returning(self):
        print("=" * 30)
        print("RETURNING")
        print("=" * 30)
        print()
        car_rented = self.file_handler.load_from_file("rented_cars.txt")
        car_found = False

        while True:
            try:
                for car in car_rented:
                    if car["customer"].lower() == self.email.lower():
                        car_found = True
                if not car_found:
                    raise CustomerNoRentsError
                break
            except CustomerNoRentsError as e:
                print(f"Error: {e}")
                self.enter_to_continue()
                print("Returning back to user menu.....")
                time.sleep(0.5)
                return

        car_id = input("Enter car id: ").strip()
        if self.quit_choice(car_id):
            return

        rental_manager = RentalManager()
        car = rental_manager.process_return(car_id, self.email)
        if not car:
            return False

        self.all_users = self.file_handler.load_from_file("users.txt")
        self.cars_rented = self.file_handler.load_from_file("rented_cars.txt")

        users = self.all_users
        for user in users:
            if user["email"].lower() == self.email.lower():
                for rent_car in self.cars_rented:
                    if rent_car["customer"].lower() == user["email"].lower():
                        self.car.brand = rent_car["brand"]
                        self.car.model = rent_car["model"]

                user["balance"] -= rental_manager.penalty_amount
                self.safe_email = user["email"].replace("@", "_at_").replace(".", "_dot_")
                customer_user = self.file_handler.load_from_file(f"users/{self.safe_email}.txt")
                for car in customer_user:
                    if car["brand"].lower()== self.car.brand.lower():
                        if car["model"].lower()== self.car.model.lower():
                            car["total_cost"] -= rental_manager.penalty_amount

                self.file_handler.save_to_file(customer_user, f"users/{self.safe_email}.txt")

                user["rented_car"] = 0
                break

        self.file_handler.save_to_file(users, f"users.txt")

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
        return True

# ----------------------------------------------USER INSPECTION--------------------------------------------
    def display_user_info(self):
        self.all_users = self.file_handler.load_from_file("users.txt")
        self.cars_rented = self.file_handler.load_from_file("rented_cars.txt")

        for user in self.all_users:
            try:
                if user["email"].lower() == self.email.lower():
                    for car in self.cars_rented:
                        if user["email"].lower() == car["customer"].lower():
                            self.car.car_id = car["car_id"]
                        else:
                            self.car.car_id = "No Car Rented Yet"
                    print (f"""
{"="*30}
      USER INFORMATION
{"="*30}
{self.bold_italics}Name{self.reset} : {user["name"]}
{self.bold_italics}Email{self.reset} : {user["email"]}
{self.bold_italics}Address{self.reset} : {user["address"]}
{self.bold_italics}Balance{self.reset} : {f"{user["balance"]} PKR" if user["balance"] > 0 else f"{user["balance"]*-1} PKR With be deducted on next deposit"}
{self.bold_italics}Rented Car ID{self.reset}: {self.car.car_id}
{"="*30}
""")
                    self.enter_to_continue()
                    print("Returning back to user menu.....")
                    time.sleep(0.5)
            except ValueError:
                print("An Error occurred. Please try again")
                print("Returning back to user menu.....")
                time.sleep(0.5)
                return

    def user_rental_history(self):
        print("=" * 30)
        print("USER RENTAL HISTORY")
        print("=" * 30)
        print()
        self.all_users = self.file_handler.load_from_file("users.txt")
        user_found = False

        while True:
            try:
                for user in self.all_users:
                    if user["email"].lower() == self.email.lower():
                        user_found = True
                        self.email = user["email"]
                if not user_found:
                    raise AccountNotFoundError
                break
            except AccountNotFoundError as e:
                print("Error:", e)
                self.enter_to_continue()
                print("Returning back to user menu.....")
                time.sleep(0.5)
                return

        self.safe_email = self.email.replace("@", "_at_").replace(".", "_dot_")
        one_user = self.file_handler.load_from_file(f"users/{self.safe_email}.txt")
        if not one_user:
            print("You don't have any rental history. Please rent a car using our system")
            self.enter_to_continue()
            print("Returning back to user menu.....")
            time.sleep(0.5)
            return

        columns = [
            ("S.No.", 5), ("Car Name", 20), ("Days", 5), ("Rental Date", 15), ("Return Date", 15),
            ("Total Cost (PKR)", 20)
        ]

        header = ""
        for col_name, width in columns:
            header += f"| {self.bold_italics}{col_name:<{width}}{self.reset}"
        print(header + "|")

        for num, rental in enumerate(one_user, start=1):
            row = f"| {num:<{columns[0][1]}}"
            row += f"| {rental['brand']+" "+rental['model']:<{columns[1][1]}}"
            row += f"| {rental['days']:<{columns[2][1]}}"
            row += f"| {rental['rental_date']:<{columns[3][1]}}"
            row += f"| {rental['return_date']:<{columns[4][1]}}"
            row += f"| {rental['total_cost']:<{columns[5][1]}}"
            print(row + "|")
        print()
        self.enter_to_continue()
        print("Returning back to user menu.....")
        time.sleep(0.5)
        return
    #------------------------------------------------INFORMATION UPDATE--------------------------------------------

    def update_balance(self):

        print("=" * 30)
        print("BALANCE UPDATE")
        print("=" * 30)
        print("Press q/Q at any time to quit")
        print()
        self.all_users = self.file_handler.load_from_file("users.txt")
        users = self.all_users
        while True:
            try:
                for user in users:
                    if user["email"].lower() == self.email.lower():
                        balance = input("Enter your balance to be updated: ")

                        if self.quit_choice(balance):
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

                        if user["balance"] < 0:
                            print(f"{-1 * user["balance"]} PKR will be deducted from your deposit")

                        user["balance"] += balance
                        self.file_handler.save_to_file(users, "users.txt")
                        print("Balance updated successfully!")
                        print(f"Updated balance: {user['balance']} PKR")
                        time.sleep(0.5)
                        print("Returning back to user menu.....")
                        time.sleep(0.5)
                        return

            except ValueError as e:
                print(f"Error: {e}")
            except OverflowError as e:
                print(f"Error: {e}")

    def update_info(self, member=None):
        print("=" * 30)
        print("UPDATE INFORMATION")
        print("=" * 30)
        print()
        print("Press q/Q at any time to quit")
        self.all_users = self.file_handler.load_from_file("users.txt")
        users = self.all_users
        while True:
            try:
                for user in users:
                    if self.email.lower() == user["email"].lower():
                        super().update_info(user)
                        password = self.password
                        user["password"] = password

                        address = input("Enter your address: ").strip()
                        if self.quit_choice(password):
                            return
                        if len(address) > 50:
                            raise OverflowError("Address cannot be more than 50 characters")

                        if address != "":
                            user["address"] = address
                        else:
                            address = user["address"]
                            user["address"] = address

                        if address.isdigit():
                            raise Exception("Address can't be just an integer")

                self.file_handler.save_to_file(users, "users.txt")
                print("Updated your information....")
                time.sleep(0.5)
                print("Saving your information....")
                time.sleep(0.5)
                print("Information updated successfully!")
                time.sleep(0.5)
                print("Returning back to user menu.....")
                time.sleep(0.5)
                return

            except PasswordError as e:
                print(f"Error: {e}")

            except OverflowError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error: {e}")

#---------------------------------------FEEDBACK-----------------------------------------------------------

    def write_feedback(self):
        feedbacks = self.file_handler.load_from_file("feedbacks.txt")
        print("=" * 30)
        print("FEEDBACK")
        print("=" * 30)
        print()
        print("We love to hear from you. Write your valuable feedback here please:")
        print("Please keep a 50 words limit")
        print()
        print("Press q/Q at any time to quit")
        print()
        while True:
            try:
                feedback = input("Feedback: ").strip()
                if feedback.isdigit():
                    raise Exception("Feedback cannot be just an integer")

                if self.quit_choice(feedback):
                    return

                if self.quit_choice(feedback):
                    return

                if not feedback:
                    raise ValueError("Feedback cannot be empty")

                if len(feedback) > 50:
                    OverflowError("Feedback cannot be more than 50 characters")
                break

            except ValueError as e:
                print(f"Error: {e}")
            except OverflowError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error: {e}")

        feedback = {
            "name" : self.name,
            "email" : self.email,
            "feedback" : feedback,
        }

        time.sleep(0.5)
        print("Thank you for your feedback!.....")
        time.sleep(0.5)
        print("Returning back to user menu.....")
        time.sleep(0.5)
        feedbacks.append(feedback)
        self.file_handler.save_to_file(feedbacks, "feedbacks.txt")
