from datetime import datetime
from vehicle.car import Car
from user.customer import User

class Rental(Car, User):
    def __init__(self, days, brand, model, seating_capacity, price_per_day, fuel_type,
                 car_type, fuel_average, first_name, last_name, password):
        Car.__init__(self, brand, model, seating_capacity, price_per_day, fuel_type, car_type, fuel_average)
        User.__init__(self, first_name, last_name, password)

        self.rental_date = datetime.now()
        self.return_date = None
        self.expected_cost = days * self.price_per_day
        self.final_cost = None
        self.days = days
        self.vehicle = {self.brand} + " " + {self.model}

    def print_receipt(self):
        return f"""
{"="*30}
    RECEIPT
{"="*30}
Customer Name : {self.name}
Car ID: {self.car_id}
Car : {self.vehicle}
Rental Date : {self.rental_date}
Expected Days : {self.days}
{"="*30}
Expected Cost: {self.expected_cost}
{"="*30}
"""
