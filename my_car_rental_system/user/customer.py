from user import User
from rental_management.rental_manager import RentalManager
from datetime import datetime

class Customer(User, RentalManager):
    def __init__(self, first_name, last_name, password, address, balance, days, brand, model, seating_capacity, price_per_day, fuel_type,
                 car_type, fuel_average):
        super().__init__(first_name, last_name, password, days, brand, model, seating_capacity, price_per_day, fuel_type,
                 car_type, fuel_average)
        self.address = address
        self.balance = balance
        self.user_rental_history = self.load_from_file("users.txt")

    def display_user_info(self):
        return f"""
{"="*30}
USER INFORMATION
{"="*30}
Name : {self.name}
Address : {self.address}
Balance : {self.balance}
{"="*30}
"""
    def renting(self):
        self.process_rental()
        renting = {
            "car_id" : self.car_id,
            "brand" : self.brand,
            "model" : self.model,
            "days" : self.days,
            "rental_date" : self.rental_date,
            "cost" : self.total_cost,
        }
        self.user_rental_history.append(renting)

    def returning(self):

        self.process_return()
        for user in self.user_rental_history:
            if user["name"] == self.name:
                for rent in user:
                    if rent["car_id"] == self.car_id:
                        rent["return_date"] = datetime.now()
                    else:
                        raise Exception("No car rented with this ID")

