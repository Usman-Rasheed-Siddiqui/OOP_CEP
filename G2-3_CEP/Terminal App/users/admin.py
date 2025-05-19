from .basic_user import User
from file_handler.file_handler import FileHandler
from exception_handling.CustomExceptions import WrongPasswordError, PasswordError, AlreadyRentedError
from vehicle.car import Car
import uuid  # For generating unique car IDs
import time


class Admin(User):
    """
    Admin class that inherits from User class.
    Handles all admin-specific operations including:
    - Admin login and authentication
    - Admin profile management
    - Adding new cars to the fleet
    """

    def __init__(self, password="", brand="", model="", seating_capacity="", price_per_day=0,
                 fuel_type="", car_type="", fuel_average="", availability=True):
        """
        Initialize Admin with car management capabilities

        Args:
            password (str): Admin password
            brand (str): Car brand (default empty)
            model (str): Car model (default empty)
            seating_capacity (str): Car seating capacity
            price_per_day (int): Daily rental price
            fuel_type (str): Type of fuel car uses
            car_type (str): Type/class of car
            fuel_average (str): Fuel efficiency
            availability (bool): Whether car is available (default True)
        """
        super().__init__(password)
        self.file_handler = FileHandler()  # For file operations
        self.admin_info = self.file_handler.load_from_file("admin_info.txt")  # Load admin credentials
        # Initialize car with provided/default parameters
        self.car = Car(brand, model, seating_capacity, price_per_day, fuel_type,
                       car_type, fuel_average, availability)
        self.cars = self.file_handler.load_from_file("cars.txt")  # All cars in system
        self.available_cars = self.file_handler.load_from_file("available_cars.txt")  # Available cars

    # ---------------------------------------------LOGIN AND ACCOUNT CREDENTIALS-----------------------------------

    def login(self):
        """Handle admin login process"""
        print("=" * 30)
        print("         LOGIN ADMIN")
        print("=" * 30)
        print()
        if not super().login():  # First perform basic user login
            return False
        # Then verify admin-specific credentials
        return self.check_admin_password()

    def update_info(self, member=None):
        """Update admin account information"""
        self.admin_info = self.file_handler.load_from_file("admin_info.txt")
        while True:
            try:
                for admin in self.admin_info:
                    super().update_info(admin)  # Use parent class update method
                    admin["password"] = self.password  # Update password
                # Save changes to file
                self.file_handler.save_to_file(self.admin_info, "admin_info.txt")
                print("Information Updated successfully")
                self.enter_to_continue()
                print("Returning back to admin menu....")
                time.sleep(0.5)
                break

            except PasswordError as e:
                print("Error:", e)

    def check_admin_password(self):
        """Verify admin password with retry mechanism"""
        self.admin_info = self.file_handler.load_from_file("admin_info.txt")
        attempts = 3  # Number of login attempts allowed

        while attempts > 0:
            try:
                for admin in self.admin_info:
                    if self.email.lower() == admin["email"].lower():
                        if self.password == admin["password"]:  # Check password match
                            self.name = admin["name"]
                            print("Password match!")
                            print(f"Welcome onboard! Mr.{self.name}")
                            time.sleep(0.5)
                            return True
                        else:
                            attempts -= 1
                            print(f"Password or name mismatch. You have {attempts} attempts left")
                            if attempts == 0:
                                raise WrongPasswordError  # No attempts left
                            print("Try again!")
                            # Get new credentials
                            self.email = input("Enter your email: ").strip()
                            if self.quit_choice(self.email):
                                return
                            self.password = input("Enter your password: ").strip()
                            if self.quit_choice(self.password):
                                return

            except PasswordError as e:
                print("Error:", e)
            except WrongPasswordError as e:
                print(f"Error: {e}")
                time.sleep(0.7)
                print("Returning back to main menu....")
                time.sleep(0.5)
                return

        return False

    # -----------------------------------ADD NEW CAR FLEET--------------------------------------------------------

    def add_new_car_fleet(self, availability=True):
        """
        Add new cars to the rental fleet

        Args:
            availability (bool): Whether cars are immediately available (default True)
        """
        print("=" * 30)
        print("        ADD NEW FLEET")
        print("=" * 30)
        print("Press q/Q at anytime to quit the process")
        print()

        # Load current car data
        self.cars = self.file_handler.load_from_file("cars.txt")
        self.available_cars = self.file_handler.load_from_file("available_cars.txt")

        # Get number of cars to add with validation
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
                print("Error:", e)
            except ValueError as e:
                print("Error:", e)

        # Get car brand with validation
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

        # Get car model with validation
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

        # Get seating capacity with validation
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
                print("Error:", e)
            except ValueError as e:
                print("Error:", e)

        # Get price per day with validation
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
                print("Error:", e)
            except ValueError as e:
                print("Error:", e)

        # Get fuel type with validation
        while True:
            try:
                self.car.fuel_type = input("Enter fuel type: ").strip()
                if self.quit_choice(self.car.fuel_type):
                    return
                if not self.car.fuel_type:
                    raise ValueError("Fuel type is required")
                break
            except ValueError as e:
                print("Error:", e)

        # Get car type with validation
        while True:
            try:
                self.car.car_type = input("Enter car type: ").strip()
                if self.quit_choice(self.car.car_type):
                    return
                if not self.car.car_type:
                    raise ValueError("Car type is required")
                break
            except ValueError as e:
                print("Error:", e)

        # Get fuel average with validation
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
                print("Error:", e)
            except ValueError as e:
                print("Error:", e)

        self.car.availability = availability
        cars = self.cars
        available_cars = self.available_cars

        # Add specified number of cars to system
        for _ in range(no_of_cars):
            car_id = str(uuid.uuid4())  # Generate unique ID for each car
            # Create car record for main cars file
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
            # Create car record for available cars file
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

        # Save updated car lists
        self.file_handler.save_to_file(cars, "cars.txt")
        self.file_handler.save_to_file(available_cars, "available_cars.txt")

        print("Saving details for new car....")
        time.sleep(0.5)
        print("Getting everything ready....")
        time.sleep(0.5)
        print("New car was added successfully....")
        time.sleep(0.5)
        self.enter_to_continue()
        print("Returning back to admin menu....")
        time.sleep(0.5)

#----------------------------------------REMOVE CAR FLEET---------------------------------------------------

    def remove_car_fleet(self):
        """
        Remove an entire fleet of available cars (same brand and model) from the system
        Only removes cars that are currently available (not rented)
        """
        print("=" * 68)
        print("                          REMOVE CAR FLEET")
        print("=" * 68)
        print()

        # Load current car data
        self.cars = self.file_handler.load_from_file("cars.txt")
        if not self.cars:
            print("No cars available right now.")
            self.enter_to_continue()
            print("Returning back to menu.....\n")
            time.sleep(0.5)
            return

        # Check for available cars
        true_car = [car for car in self.cars if car["availability"]]
        if not true_car:
            print("No cars available right now.")
            self.enter_to_continue()
            print("Returning back to menu.....\n")
            time.sleep(0.5)
            return

        self.available_cars = self.file_handler.load_from_file("available_cars.txt")
        if not self.available_cars:
            print("No cars available right now.")
            self.enter_to_continue()
            print("Returning back to menu   .....\n")
            time.sleep(0.5)
            return

        # Display available cars and get user input
        self.car.display_available_cars_names()
        print()
        print("Press q/Q at anytime to quit the process")
        print()

        # Get brand name with validation
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

        # Get model name with validation
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

        # Filter out the cars to be removed
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

        # Save updated lists
        self.file_handler.save_to_file(available_cars, "available_cars.txt")
        self.file_handler.save_to_file(cars, "cars.txt")
        print("Please Note: Only those cars of the fleets will be removed")
        print("if they are not rented. The rented ones can be removed later when returned")
        time.sleep(0.5)
        print("Cars successfully removed....")
        self.enter_to_continue()
        print("Returning back to admin menu....")
        time.sleep(0.5)

    def remove_specific_car(self):
        """
        Remove a specific car from the system by its ID
        Only removes cars that are currently available (not rented)
        """
        print("=" * 30)
        print("REMOVE SPECIFIC CAR")
        print("=" * 30)
        print("Press q/Q at anytime to quit the process")
        print()

        # Load and check car data
        self.cars = self.file_handler.load_from_file("cars.txt")
        true_cars = [car for car in self.cars if car["availability"]]
        if not true_cars:
            print("No available cars were found to be removed")
            self.enter_to_continue()
            print("Returning back to admin menu....")
            time.sleep(0.5)
            return

        self.available_cars = self.file_handler.load_from_file("available_cars.txt")
        if not self.available_cars:
            print("No available cars were found to be removed")
            self.enter_to_continue()
            print("Returning back to admin menu....")
            time.sleep(0.5)
            return

        # Get car ID to remove
        car_found = False
        while True:
            try:
                car_id = input("Enter car id of the car to be removed: ").strip()
                if self.quit_choice(car_id):
                    return
                if not car_id:
                    raise ValueError("Car id is required")

                # Check if car exists and can be removed
                for car in self.cars:
                    if car["car_id"] == car_id:
                        car_found = True
                        if not car["availability"]:
                            raise AlreadyRentedError("This car is currently rented. It cannot be removed")
                        self.cars.remove(car)
                        self.available_cars = [car for car in self.available_cars if not car["car_id"] == car_id]

                if not car_found:
                    raise Exception("No car with this id found")

                break
            except ValueError as e:
                print("Error:", e)
            except AlreadyRentedError as e:
                print("Error:", e)
                print("Returning back to admin menu....")
                time.sleep(0.5)
                return
            except Exception as e:
                print("Error:", e)

            # Save changes
            self.file_handler.save_to_file(self.available_cars, "available_cars.txt")
            self.file_handler.save_to_file(self.cars, "cars.txt")
            print("Removing Car.....")
            time.sleep(0.5)
            print("Just a Moment.....")
            time.sleep(0.5)
            print("Car removed successfully....")
            self.enter_to_continue()
            print("Returning back to admin menu....")
            time.sleep(0.5)
            return

    def display_car_id(self):
        """
        Display all cars in the system with their IDs and availability status
        """
        print("=" * 92)
        print("                                     DISPLAY ALL CARs ID")
        print("=" * 92)
        print()

        # Load and display car data in formatted table
        self.cars = self.file_handler.load_from_file("cars.txt")
        columns = [
            ("S.No.", 5), ("Brand", 15), ("Model", 15), ("Car ID", 40), ("Availability", 15)
        ]

        # Print table header
        header = ""
        for col_name, width in columns:
            header += f"| {self.bold_italics}{col_name:<{width}}{self.reset}"
        print(header + "|")

        # Print each car's information
        for num, car in enumerate(self.cars, start=1):
            row = f"| {num:<{columns[0][1]}}"
            row += f"| {car['brand']:<{columns[1][1]}}"
            row += f"| {car['model']:<{columns[2][1]}}"
            row += f"| {car['car_id']:<{columns[3][1]}}"
            row += f"| {'Available' if car['availability'] else 'Not Available':<{columns[4][1]}}"
            print(row + "|")

        print()
        self.enter_to_continue()
        print("Returning back to admin menu....")
        time.sleep(0.5)
        return

    # ----------------------------------------ACCESS FEEDBACKS----------------------------------------------------
    def access_feedbacks(self):
        """
        Display all customer feedbacks in a formatted table
        """
        print("=" * 105)
        print("                                                FEEDBACKS")
        print("=" * 105)
        print()

        # Load and display feedback data
        feedbacks = self.file_handler.load_from_file("feedbacks.txt")
        columns = [
            ("S.No.", 5), ("Name", 20), ("Email", 25), ("Feedback", 55),
        ]

        # Print table header
        header = ""
        for col_name, width in columns:
            header += f"|{self.bold_italics}{col_name:<{width}}{self.reset} "
        print(header + "|")

        # Print each feedback
        for num, feedback in enumerate(feedbacks, start=1):
            row = f"| {num:>{columns[0][1]}}"
            row += f"|{feedback['name']:<{columns[1][1]}} "
            row += f"|{feedback['email']:<{columns[2][1]}} "
            row += f"|{feedback['feedback']:<{columns[3][1]}}"
            print(row + "|")

        self.enter_to_continue()
        print("Returning back to admin menu....")
        time.sleep(0.5)

    def display_user_info(self):
        """
        Display rental history for a specific user by email
        """
        print("=" * 130)
        print("                                                    DISPLAY USER RENTAL HISTORY")
        print("=" * 130)
        print()

        # Load user data and get email input
        users = self.file_handler.load_from_file("users.txt")
        email_found = False
        print("Press q/Q at anytime to quit the process")

        while True:
            try:
                self.email = input("Enter Email of User: ").strip()
                if self.quit_choice(self.email):
                    return

                if not self.email:
                    raise ValueError("Email cannot be empty")

                # Verify user exists
                for user in users:
                    if user["email"].lower() == self.email.lower():
                        email_found = True
                        self.name = user["name"]
                        self.email = user["email"]

                if not email_found:
                    raise ValueError("No user with this email found")
                break
            except ValueError as e:
                print("Error:", e)

        # Load user's rental history
        safe_email = self.email.replace("@", "_at_").replace(".", "_dot_")
        one_user = self.file_handler.load_from_file(f"users/{safe_email}.txt")

        if not one_user:
            print("User does not have a rental history yet")
            self.enter_to_continue()
            print("Returning back to admin menu....")
            time.sleep(0.5)
            return

        # Display rental history in formatted table
        columns = [
            ("S.No.", 5), ("Car ID", 40), ("Brand", 15), ("Model", 15), ("Days", 5), ("Rental Date", 15),
            ("Return Date", 15), ("Total Cost (PKR)", 20)
        ]

        print(f"{self.bold_italics}Name:{self.reset} {self.name}")
        print(f"{self.bold_italics}Email:{self.reset} {self.email}")
        print()

        # Print table header
        header = ""
        for col_name, width in columns:
            header += f"| {self.bold_italics}{col_name:<{width}}{self.reset}"
        print(header + "|")

        # Print each rental record
        for num, rental in enumerate(one_user, start=1):
            row = f"|{num:<{columns[0][1]}} "
            row += f"|{rental['car_id']:<{columns[1][1]}} "
            row += f"|{rental['brand']:<{columns[2][1]}} "
            row += f"|{rental['model']:<{columns[3][1]}} "
            row += f"|{rental['days']:<{columns[4][1]}} "
            row += f"|{rental['rental_date']:<{columns[5][1]}} "
            row += f"|{rental['return_date']:<{columns[6][1]}} "
            row += f"|{rental['total_cost']:<{columns[7][1]}} "
            print(row + "|")

        self.enter_to_continue()
        print("Returning back to admin menu....")
        time.sleep(0.5)
        return

    def check_current_rentals(self):
        """
        Display all currently rented cars with tenant information
        """
        print("=" * 170)
        print("                                                                          CHECK CURRENT RENTALS")
        print("=" * 170)
        print()

        # Load and check rental data
        current_rentals = self.file_handler.load_from_file("rented_cars.txt")
        if not current_rentals:
            print("No car is rented right now")
            print("Returning back to admin menu....")
            time.sleep(0.5)
            return

        # Display rental count and details
        count_current_rentals = len(current_rentals)
        print(f"{self.bold_italics}Current Rentals{self.reset}: {count_current_rentals}")
        time.sleep(0.5)

        columns = [
            ("S.No.", 5), ("Name", 20), ("Email", 25), ("Car ID", 40), ("Brand", 15), ("Model", 15),
            ("Rental Date", 15), ("Return Date", 15), ("Days", 5), ("Total Cost (PKR)", 15)
        ]

        # Print table header
        header = ""
        for col_name, width in columns:
            header += f"| {self.bold_italics}{col_name:<{width}}{self.reset}"
        print(header + "|")

        # Print each rental record
        for num, car in enumerate(current_rentals, start=1):
            self.email = car["customer"]
            row = f"| {num:<{columns[0][1]}}"
            row += f"| {self.find_name(self.email):<{columns[1][1]}}"
            row += f"| {car['customer']:<{columns[2][1]}}"
            row += f"| {car['car_id']:<{columns[3][1]}}"
            row += f"| {car['brand']:<{columns[4][1]}}"
            row += f"| {car['model']:<{columns[5][1]}}"
            row += f"| {car['rental_date']:<{columns[6][1]}}"
            row += f"| {car['return_date']:<{columns[7][1]}}"
            row += f"| {car['total_days']:<{columns[8][1]}}"
            row += f"| {car['total_cost']:<{columns[9][1]}} "
            print(row + "|")

        self.enter_to_continue()
        print("Returning back to admin menu....")
        time.sleep(0.5)
        return

    def find_name(self, email):
        """
        Helper method to find user's name by email
        Args:
            email (str): User's email address
        Returns:
            str: User's full name
        """
        users = self.file_handler.load_from_file("users.txt")

        for user in users:
            if email == user["email"]:
                self.name = user["name"]

        return self.name

    def display_all_users(self):
        """
        Display all registered users with their basic information
        """
        print("=" * 170)
        print("                                                                         DISPLAY USER INFORMATION")
        print("=" * 170)

        # Load and check user data
        users = self.file_handler.load_from_file("users.txt")
        if not users:
            print("No User found")
            print("Returning back to admin menu....")
            time.sleep(0.5)
            return

        # Display user information in formatted table
        columns = [
            ("S.No.", 5), ("Name", 45), ("Email", 40), ("Address", 50), ("Balance (PKR)", 15), ("Rented Car", 15)
        ]

        # Print table header
        header = ""
        for col_name, width in columns:
            header += f"| {self.bold_italics}{col_name:<{width}}{self.reset}"
        print(header + "|")

        # Print each user's information
        for num, user in enumerate(users, start=1):
            row = f"| {num:<{columns[0][1]}}"
            row += f"| {user['name']:<{columns[1][1]}}"
            row += f"| {user['email']:<{columns[2][1]}}"
            row += f"| {user['address']:<{columns[3][1]}}"
            row += f"| {user['balance']:<{columns[4][1]}}"
            row += f"| {'Car Rented' if user['rented_car'] > 0 else 'No Car Rented':<{columns[5][1]}}"
            print(row + "|")

        self.enter_to_continue()
        print("Returning back to admin menu....")
        time.sleep(0.5)
        return

    def display_reserved_cars(self):
        """
        Display all currently reserved/rented cars with rental details
        """
        print("=" * 120)
        print("                                                 DISPLAY RESERVED CARS")
        print("=" * 120)
        print()

        # Load and check rental data
        cars_rented = self.file_handler.load_from_file("rented_cars.txt")
        if not cars_rented:
            print("No rented cars found")
            print("Returning back to admin menu....")
            time.sleep(0.5)
            return

        # Display rental information in formatted table
        columns = [
            ("S.No.", 5), ("Car Name", 20), ("Tenant Email", 40), ("Rental Date", 15), ("Return Date", 15), ("Days", 5),
            ("Total Cost (PKR)", 20)
        ]

        # Display Header
        header = ""
        for col_name, width in columns:
            header += f"| {self.bold_italics}{col_name:<{width}}{self.reset}"
        print(header + "|")

        # Display Rental Details
        for num, rental in enumerate(cars_rented, start=1):
            row = f"| {num:<{columns[0][1]}}"
            row += f"| {rental['brand'] + " " + rental['model']:<{columns[1][1]}}"
            row += f"| {rental['customer']:<{columns[2][1]}}"
            row += f"| {rental['rental_date']:<{columns[3][1]}}"
            row += f"| {rental['return_date']:<{columns[4][1]}}"
            row += f"| {rental['total_days']:<{columns[5][1]}}"
            row += f"| {rental['total_cost']:<{columns[6][1]}}"
            print(row + "|")
        print()
        self.enter_to_continue()
        print("Returning back to admin menu....")
        time.sleep(0.5)
        return