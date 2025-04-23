from datetime import datetime
from vehicle.car import Car
from user.customer import Customer


class Rental:
    def __init__(self, days, car: Car, customer: Customer):
        self.car = car
        self.customer = customer
        self.rental_date = datetime.now()
        self.return_date = None
        self.expected_cost = days * self.car.price_per_day
        self.final_cost = None
        self.days = days
        self.vehicle = {self.car.brand} + " " + {self.car.model}

    def print_receipt(self):
        return f"""
{"="*30}
    RECEIPT
{"="*30}
Customer Name : {self.customer.first_name} {self.customer.last_name}
Car ID: {self.car.car_id}
Car : {self.vehicle}
Rental Date : {self.rental_date}
Expected Days : {self.days}
{"="*30}
Expected Cost: {self.expected_cost}
{"="*30}
"""