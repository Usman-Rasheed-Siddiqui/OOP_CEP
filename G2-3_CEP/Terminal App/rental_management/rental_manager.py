import time
from datetime import datetime, timedelta
from file_handler.file_handler import FileHandler
from exception_handling.CustomExceptions import CarNotAvailableError, CarNotRentedError, InsufficientBalanceError, \
    CustomerNoRentsError
from vehicle.car import Car


class RentalManager:
    """
    Manages the car rental and return processes including:
    - Handling rental transactions
    - Calculating penalties for late returns
    - Processing car returns
    - Generating rental receipts
    """

    def __init__(self, brand="", model="", car_id=""):
        """Initialize rental manager with car details and load necessary data"""
        self.car = Car(brand, model)  # Car object to manage
        self.car_id = car_id  # Unique identifier for the car
        self.rental_date = None  # Date when car is rented
        self.return_date = None  # Expected return date
        self.actual_date = None  # Actual return date
        self.days = 0  # Number of rental days
        self.total_cost = 0  # Total rental cost
        self.penalty_amount = 0  # Late return penalty amount
        self.file_handler = FileHandler()  # For file operations

        # Load all necessary data files
        self.cars = self.file_handler.load_from_file("cars.txt")  # All cars in system
        self.users = self.file_handler.load_from_file("users.txt")  # All users
        self.rented_cars = self.file_handler.load_from_file("rented_cars.txt")  # Currently rented cars
        self.available_cars = self.file_handler.load_from_file("available_cars.txt")  # Available cars

    # ------------------------------------------------RENTING PROCESS-------------------------------------------

    def process_rental(self, customer):
        """
        Process the complete car rental transaction
        """
        # Reload latest data from files
        self.cars = self.file_handler.load_from_file("cars.txt")
        self.users = self.file_handler.load_from_file("users.txt")
        self.rented_cars = self.file_handler.load_from_file("rented_cars.txt")
        self.available_cars = self.file_handler.load_from_file("available_cars.txt")

        # Separate available and unavailable cars
        not_available_cars = [car for car in self.cars if not car["availability"]]
        available_cars = [car for car in self.cars if car["availability"]]
        found = False  # Flag to track if car was found

        try:
            # Find the requested car
            for car in available_cars:
                if (car["brand"].lower() == self.car.brand.lower() and
                        car["model"].lower() == self.car.model.lower()):

                    # Get rental duration from user
                    while True:
                        try:
                            self.days = int(input("Enter the number of days to rent the car: "))
                            if self.days > 0:
                                break
                            print("Please enter valid number of days")
                        except ValueError:
                            print("Error: Please enter number of days.")

                    # Store car details
                    self.car.brand = car["brand"]
                    self.car.model = car["model"]
                    found = True
                    self.total_cost = self.days * car["price_per_day"]

                    # Check customer balance
                    for user in self.users:
                        if user["email"].lower() == customer.lower():
                            if user["balance"] < self.total_cost:
                                raise InsufficientBalanceError(
                                    "Your balance is insufficient. Please update your balance to make a rent")

                    self.car_id = car["car_id"]
                    break

            if not found:
                raise CarNotAvailableError

        except CarNotAvailableError as e:
            print(f"Error: {e}")
            print("Returning back to main menu.....")
            time.sleep(0.5)
            return False
        except InsufficientBalanceError as e:
            print("Error:", e)
            return False

        # Set rental dates
        self.rental_date = datetime.now().date()
        self.return_date = self.rental_date + timedelta(days=self.days)

        # Create rental record
        rental = {
            "car_id": self.car_id,
            "customer": customer,
            "brand": self.car.brand,
            "model": self.car.model,
            "rental_date": str(self.rental_date),
            "return_date": str(self.return_date),
            "total_days": self.days,
            "total_cost": self.total_cost,
        }

        # Update system records
        self.rented_cars.append(rental)

        # Remove from available cars
        for car in self.available_cars:
            if car["car_id"] == self.car_id:
                self.available_cars.remove(car)
                break

        # Mark car as unavailable
        for car in self.cars:
            if car["car_id"] == self.car_id:
                car["availability"] = False
                break

        # Save all changes
        all_cars = self.cars + not_available_cars
        self.file_handler.save_to_file(all_cars, "cars.txt")
        self.file_handler.save_to_file(self.rented_cars, "rented_cars.txt")
        self.file_handler.save_to_file(self.available_cars, "available_cars.txt")

        return rental

    # ------------------------------------------PENALTY MANAGEMENT------------------------------------------------

    def penalty(self, actual_date, return_date, car, users, customer):
        """
        Calculate penalty for late return
        """
        if actual_date <= return_date:
            self.total_cost = car["total_cost"]
            return 0  # No penalty if returned on or before due date
        else:
            extra = 1000  # Daily penalty rate
            days_difference = (actual_date - return_date).days
            penalty = extra * days_difference

            # Notify customer about penalty
            for user in users:
                if user["email"].lower() == customer.lower():
                    if self.penalty_balance_comparision(user["balance"], penalty):
                        print("You have used the car more than the rental date")
                        print("decided. We will charge extra amount....")
                        time.sleep(0.5)
                        print(f"An amount of {penalty} PKR is being deducted from your balance.....")
                        time.sleep(0.5)

            return penalty

    def penalty_balance_comparision(self, balance, penalty):
        """
        Check if customer balance can cover penalty
        """
        if balance > penalty:
            return True
        elif balance < penalty:
            print("You have used the car more than the rental date")
            print("decided. We will charge extra amount....")
            time.sleep(0.5)
            print("Your balance is less than the penalty amount...")
            time.sleep(0.5)
            print(f"{penalty - balance} PKR will be deducted on the next deposit..")
            time.sleep(0.5)
        return False

    # ---------------------------------------------RETURNING PROCESS---------------------------------------------

    def process_return(self, car_id, customer):
        """
        Process car return transaction
        """
        # Reload latest data
        self.cars = self.file_handler.load_from_file("cars.txt")
        self.users = self.file_handler.load_from_file("users.txt")
        self.rented_cars = self.file_handler.load_from_file("rented_cars.txt")
        self.available_cars = self.file_handler.load_from_file("available_cars.txt")

        car_found = False  # Flag to track if car was found in rentals

        try:
            # Find the rented car
            for car in self.rented_cars:
                if car["car_id"] == car_id:
                    car_found = True
                    self.days = car["total_days"]
                    self.return_date = datetime.strptime(car["return_date"], "%Y-%m-%d").date()
                    self.car.brand = car["brand"]
                    self.car.model = car["model"]

                    # Calculate penalty if any
                    self.actual_date = datetime.now().date()
                    self.penalty_amount = self.penalty(
                        self.actual_date, self.return_date, car, self.users, customer)
                    break

            if not car_found:
                raise CarNotRentedError

        except CarNotRentedError as e:
            print("Error:", e)
            time.sleep(0.5)
            print("Returning back to user menu.....")
            time.sleep(0.5)
            return None

        # Create return record
        giveaway = {
            "car_id": car_id,
            "customer": None,
            "brand": self.car.brand,
            "model": self.car.model,
            "rental_data": None,
            "return_date": None,
            "total_days": 0,
            "total_cost": 0,
        }

        # Update system records
        self.available_cars.append(giveaway)

        for car in self.cars:
            if car["car_id"] == giveaway["car_id"]:
                car["availability"] = True  # Mark car as available again
                break

        # Save all changes
        self.file_handler.save_to_file(self.available_cars, "available_cars.txt")
        self.file_handler.save_to_file(self.rented_cars, "rented_cars.txt")
        self.file_handler.save_to_file(self.cars, "cars.txt")

        return giveaway

    # --------------------------------------------RECEIPT GENERATION--------------------------------------------

    def print_receipt(self, customer):
        """
        Generate and print rental receipt
        """
        print(f"""
{"=" * 51}
                      RECEIPT
{"=" * 51}
{self.car.bold_italics}Customer Name{self.car.reset} : {customer}
{self.car.bold_italics}Car ID{self.car.reset} : {self.car_id}
{self.car.bold_italics}Car{self.car.reset} : {self.car.brand} {self.car.model}
{self.car.bold_italics}Rental Date{self.car.reset} : {self.rental_date}
{self.car.bold_italics}Return Date{self.car.reset} : {self.return_date}
{self.car.bold_italics}Total Days{self.car.reset} : {self.days}
{"=" * 51}
{self.car.bold_italics}Total Cost{self.car.reset} : {self.total_cost}
{"=" * 51}
""")
        print("Note: Please take a screenshot of receipt. You can also find Car ID in your Check Status")
        print("You will be needing your Car ID during returning")