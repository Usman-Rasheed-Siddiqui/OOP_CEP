from datetime import datetime
from rental import Rental
from vehicle.car import Car
from user.customer import Customer
from file_handler.file_handler import FileHandler

class RentalManager(Rental):
    def __init__(self, days, car: Car, customer: Customer):
        super().__init__(days, car, customer)
        self.total_cost = self.days * self.car.price_per_day
        self.file_handler = FileHandler()

        self.available_cars =self.file_handler.load_from_file("available_cars.txt")
        self.rented_cars = self.file_handler.load_from_file("rented_cars.txt")
        self.rental_history = self.file_handler.load_from_file(f"car_rental_history/{self.car.brand}_{self.car.model}.txt")


    def save_rental_history(self):
        """For saving a vehicle's rental history"""
        history = {
            "Renting Date": {self.rental_date},
            "Return Date": {self.return_date},
            "Days": {self.days},
            "Total Cost": {self.total_cost},
        }                           # Needs attributes from Rentals
        self.rental_history.append(history)
        return history

    def print_rental_history(self):
        """Printing the rental history"""
        for num,rents in enumerate(self.rental_history):
            print(f"{num}.",end=" ")
            for att, specification in rents.items():
                print(f"{att} : {rents}", end =" | ")


    def display_user_info(self):
        pass

    def process_rental(self):

        rental = {
            "car_id": {self.car.car_id},
            "customer": {self.customer.name},
            "car": {self.vehicle},
            "rental_data": {self.rental_date},
            "return_date": {self.return_date},
            "expected_days": {self.days},
            "expected_cost": {self.expected_cost},
        }
        for car in self.rented_cars:
            if car["car_id"] != rental["car_id"]:
                self.rented_cars.append(car)

        for car in self.available_cars:
            if car["car_id"] == rental["car_id"]:
                self.available_cars.remove(car)

        self.file_handler.save_to_file(self.available_cars, "available_cars.txt")
        self.file_handler.save_to_file(self.rented_cars, "rented_cars.txt")

        return rental

    def process_return(self):

        self.days = self.return_date - self.rental_date

        giveaway = {
            "car_id": {self.car.car_id},
            "customer": {self.customer.name},
            "car": {self.vehicle},
            "rental_data": {self.rental_date},
            "return_date": datetime.now(),
            "total_days": {self.days},
            "total_cost": {self.total_cost},
        }

        for car in self.available_cars:
            if car["car_id"] != giveaway["car_id"]:
                self.available_cars.append(car)

        for car in self.rented_cars:
            if car["car_id"] == giveaway["car_id"]:
                self.rented_cars.remove(car)

        self.file_handler.save_to_file(self.available_cars, "available_cars.txt")
        self.file_handler.save_to_file(self.rented_cars, "rented_cars.txt")

        return giveaway

