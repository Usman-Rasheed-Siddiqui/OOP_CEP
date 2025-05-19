import time
from datetime import datetime, timedelta
from file_handler.file_handler import FileHandler
from exception_handling.CustomExceptions import CarNotAvailableError, CarNotRentedError, InsufficientBalanceError, CustomerNoRentsError
from vehicle.car import Car

class RentalManager:
    def __init__(self, brand="", model="", car_id=""):
        self.car = Car(brand, model)
        self.car_id = car_id
        self.rental_date = None
        self.return_date = None
        self.actual_date = None
        self.days = 0
        self.total_cost = 0
        self.penalty_amount = 0
        self.file_handler = FileHandler()
        self.cars = self.file_handler.load_from_file("cars.txt")
        self.users = self.file_handler.load_from_file("users.txt")
        self.rented_cars = self.file_handler.load_from_file("rented_cars.txt")
        self.available_cars = self.file_handler.load_from_file("available_cars.txt")

#------------------------------------------------RENTING PROCESS-------------------------------------------

    def process_rental(self, customer):
        self.cars = self.file_handler.load_from_file("cars.txt")
        self.users = self.file_handler.load_from_file("users.txt")
        self.rented_cars = self.file_handler.load_from_file("rented_cars.txt")
        self.available_cars = self.file_handler.load_from_file("available_cars.txt")

        cars = self.cars
        users = self.users
        rented_cars = self.rented_cars
        available_cars = self.available_cars

        not_available_cars = [car for car in cars if car["availability"] == False]
        cars = [car for car in cars if car["availability"] == True]
        found = False

        try:
            for car in cars:
                if car["brand"].lower() == self.car.brand.lower() and car["model"].lower() == self.car.model.lower():
                    while True:
                        try:
                            self.days = int(input("Enter the number of days to rent the car: "))
                            if self.days > 0:
                                break
                            else:
                                print("Please enter valid number of days")
                        except ValueError:
                            print("Error: Please enter number of days.")

                    self.car.brand = car["brand"]
                    self.car.model = car["model"]
                    found = True
                    self.total_cost = self.days * car["price_per_day"]
                    try:
                        for user in users:
                            if user["email"].lower() == customer.lower():
                                if user["balance"] < self.total_cost:
                                    raise InsufficientBalanceError("Your balance is insufficient. Please update your balance to make a rent")
                    except InsufficientBalanceError as e:
                        print("Error:", e)
                        return False

                    self.car_id = car["car_id"]
                    break
            if not found:
                raise CarNotAvailableError

        except CarNotAvailableError as e:
            print(f"Error: {e}")
            print("Returning back to main menu.....")
            time.sleep(0.5)
            return

        self.rental_date = datetime.now().date()
        self.return_date = self.rental_date + timedelta(days=self.days)

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

        rented_cars.append(rental)

        for car in available_cars:
            if car["car_id"] == self.car_id:
                available_cars.remove(car)
                break

        for car in cars:
            if car["car_id"] == self.car_id:
                car["availability"] = False
                break

        all_cars = cars + not_available_cars

        self.file_handler.save_to_file(all_cars, "cars.txt")
        self.file_handler.save_to_file(rented_cars, "rented_cars.txt")
        self.file_handler.save_to_file(available_cars, "available_cars.txt")
        return rental

#------------------------------------------PENALTY MANAGEMENT------------------------------------------------

    def penalty(self, actual_date, return_date, car, users, customer):

        if actual_date <= return_date:
            self.total_cost = car["total_cost"]
            return 0
        else:
            extra = 1000
            days_difference = (actual_date - return_date).days
            penalty = extra * days_difference

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
        return

#---------------------------------------------RETURNING PROCESS---------------------------------------------

    def process_return(self, car_id, customer):

        self.cars = self.file_handler.load_from_file("cars.txt")
        self.users = self.file_handler.load_from_file("users.txt")
        self.rented_cars = self.file_handler.load_from_file("rented_cars.txt")
        self.available_cars = self.file_handler.load_from_file("available_cars.txt")

        rented_cars = self.rented_cars
        available_cars = self.available_cars
        cars = self.cars
        users = self.users
        car_found = False

        try:
            for car in rented_cars:
                if car["car_id"] == car_id:
                        car_found = True
                        self.days = car["total_days"]
                        self.return_date = datetime.strptime(car["return_date"], "%Y-%m-%d").date()
                        self.car.brand = car["brand"]
                        self.car.model = car["model"]

                        self.actual_date = datetime.now().date()
                        self.penalty_amount = self.penalty(self.actual_date, self.return_date, car, users, customer)
                        break

            if not car_found:
                raise CarNotRentedError

        except CarNotRentedError as e:
            print("Error:", e)
            time.sleep(0.5)
            print("Returning back to user menu.....")
            time.sleep(0.5)
            return

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

        available_cars.append(giveaway)

        for car in cars:
            if car["car_id"] == giveaway["car_id"]:
                car["availability"] = True
                break

        self.file_handler.save_to_file(available_cars, "available_cars.txt")
        self.file_handler.save_to_file(rented_cars, "rented_cars.txt")
        self.file_handler.save_to_file(cars, "cars.txt")

        return giveaway

#--------------------------------------------RECEIPT GENERATION--------------------------------------------

    def print_receipt(self, customer):
        print(f"""
{"="*51}
                      RECEIPT
{"="*51}
{self.car.bold_italics}Customer Name{self.car.reset} : {customer}
{self.car.bold_italics}Car ID{self.car.reset} : {self.car_id}
{self.car.bold_italics}Car{self.car.reset} : {self.car.brand} {self.car.model}
{self.car.bold_italics}Rental Date{self.car.reset} : {self.rental_date}
{self.car.bold_italics}Return Date{self.car.reset} : {self.return_date}
{self.car.bold_italics}Total Days{self.car.reset} : {self.days}
{"="*51}
{self.car.bold_italics}Total Cost{self.car.reset} : {self.total_cost}
{"="*51}
""")
        print("Note: Please take a screenshot of receipt. You can also find Car ID in your Check Status")
        print("You will be needing your Car ID during returning")
