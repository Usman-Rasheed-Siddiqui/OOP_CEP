import time
from datetime import datetime, timedelta
from file_handler.file_handler import FileHandler
from exception_handling.Exceptions import CarNotAvailableError, CarNotRentedError, InsufficientBalanceError, CustomerNoRentsError
from vehicle.car import Car

class RentalManager:
    def __init__(self, brand="", model="", car_id="", expected_cost=0):
        self.car = Car(brand, model)
        self.car_id = car_id
        self.rental_date = None
        self.return_date = None
        self.days = 0
        self.expected_cost = expected_cost
        self.total_cost = 0
        self.penalty_amount = 0
        self.file_handler = FileHandler()
        self.cars = self.file_handler.load_from_file("cars.txt")
        self.users = self.file_handler.load_from_file("users.txt")
        self.rented_cars = self.file_handler.load_from_file("rented_cars.txt")
        self.available_cars = self.file_handler.load_from_file("available_cars.txt")

    # def save_rental_history(self):
    #     """For saving a vehicle's rental history"""
    #     for car in self.available_cars:
    #         if car["brand"] == self.brand and car["model"] == self.model:
    #             self.expected_cost = self.days * car.price_per_day
    #
    #     history = {
    #         "Renting Date": {self.rental_date},
    #         "Return Date": {self.return_date},
    #         "Days": {self.days},
    #         "Total Cost": {self.final_cost},
    #     }
    #
    #     self.file_handler.save_to_file(history,f"car_rental_history/{self.brand}_{self.model}.txt")
    #     return history


    # def print_rental_history(self):
    #     """Printing the rental history"""
    #     rental_history = self.file_handler.load_from_file(f"car_rental_history/{self.brand}_{self.model}.txt")
    #     for num,rents in zip(range(1, len(rental_history)+1),rental_history):
    #         print(f"{num}.",end=" ")
    #         for att, specification in rents.items():
    #             print(f"{att} : {rents}", end =" | ")
    #         print()

#------------------------------------------------RENTING PROCESS-------------------------------------------

    def process_rental(self, customer):

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
                            if user["name"] == customer:
                                if user["balance"] < self.total_cost:
                                    raise InsufficientBalanceError("Your balance is insufficient. Please update your balance to make a rent")
                    except InsufficientBalanceError as e:
                        print("Error:", e)

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
        else:
            extra = 20
            actual_days = (actual_date - return_date).days
            days_difference = actual_days - self.days
            penalty = extra * days_difference

            self.total_cost += penalty

            for user in users:
                if user["name"] == customer:

                    if self.penalty_balance_comparision(user["balance"], penalty):
                        user["balance"] -= penalty
                        print("You have used the car more than the rental date...")
                        time.sleep(0.4)
                        print("decided. We will charge extra amount....")
                        time.sleep(0.4)
                        print(f"You have to pay {penalty} PKR more.....")
                        time.sleep(0.4)
                        print(f"Total amount is now: {self.total_cost}...")
                        time.sleep(0.4)

    def penalty_balance_comparision(self, balance, penalty):
        if balance > penalty:
            return True
        elif balance < penalty:
            print("Your balance is less than the penalty amount...")
            time.sleep(0.4)
            print(f"{self.penalty_amount} will be deducted on the next deposit..")
            time.sleep(0.5)
        return

#---------------------------------------------RETURNING PROCESS---------------------------------------------

    def process_return(self, car_id, customer):

        rented_cars = self.rented_cars
        available_cars = self.available_cars
        cars = self.cars
        safe_name = customer.replace(" ", "_")
        user_rental_history = self.file_handler.load_from_file(f"users/{safe_name}.txt")
        users = self.users
        customer_found = False
        car_found = False

        try:
            for car in rented_cars:
                if car["car_id"] == car_id:
                    car_found = True
                    if car["customer"].lower() == customer.lower():
                        customer_found = True

                        self.days = car["total_days"]
                        self.return_date = datetime.strptime(car["return_date"], "%Y-%m-%d").date()
                        self.car.brand = car["brand"]
                        self.car.model = car["model"]

                        actual_date = datetime.now().date()
                        self.penalty(actual_date, self.return_date, car, users, customer)
                        break

            if not customer_found:
                raise CustomerNoRentsError
            if not car_found:
                raise CarNotRentedError

        except CustomerNoRentsError as e:
            print("Error:", e)
            return
        except CarNotRentedError as e:
            print("Error:", e)
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

        for car in user_rental_history:
            if car["car_id"] == car_id:
                car["total_cost"] = self.total_cost

        for car in cars:
            if car["car_id"] == giveaway["car_id"]:
                car["availability"] = True
                break

        for car in rented_cars:
            if car["car_id"] == giveaway["car_id"]:
                rented_cars.remove(car)

        self.file_handler.save_to_file(users, "users.txt")
        self.file_handler.save_to_file(user_rental_history, f"users/{safe_name}.txt")
        self.file_handler.save_to_file(available_cars, "available_cars.txt")
        self.file_handler.save_to_file(rented_cars, "rented_cars.txt")
        self.file_handler.save_to_file(cars, "cars.txt")

        return giveaway

#--------------------------------------------RECEIPT GENERATION--------------------------------------------

    def print_receipt(self, customer):
        print(f"""
{"="*38}
            RECEIPT
{"="*38}
Customer Name : {customer}
Car ID: {self.car_id}
Car : {self.car.brand} {self.car.model}
Rental Date : {self.rental_date}
Return Date : {self.return_date}
Total Days : {self.days}
{"="*30}
Total Cost: {self.total_cost}
{"="*38}
""")
        print("Note: Please take a screenshot of receipt to remember the Car ID when returning")
