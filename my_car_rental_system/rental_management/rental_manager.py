from datetime import datetime
from rental import Rental

class RentalManager(Rental):
    def __init__(self, days, brand, model, seating_capacity, price_per_day, fuel_type,
                 car_type, fuel_average, first_name, last_name, password):
        super().__init__(days, brand, model, seating_capacity, price_per_day, fuel_type,
                 car_type, fuel_average, first_name, last_name, password)

        self.available_cars =self.load_from_file("available_cars.txt")
        self.rented_cars = self.load_from_file("rented_cars.txt")
        self.rental_history = self.load_from_file(f"car_rental_history/{self.brand}_{self.model}.txt")


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
            "car_id": {self.car_id},
            "customer": {self.name},
            "car": {self.vehicle},
            "rental_data": {self.rental_date},
            "return_date": {self.return_date},
            "expected_days": {self.days},
            "expected_cost": {self.expected_cost},
        }

        self.available_cars.remove(rental["car_id"])
        self.rented_cars.append(rental["car_id"])
        self.save_to_file(self.available_cars, "available_cars.txt")
        self.save_to_file(self.rented_cars, "rented_cars.txt")

        return rental

    def process_return(self):

        self.days = self.return_date - self.rental_date
        self.total_cost = self.days * self.price_per_day

        giveaway = {
            "car_id": {self.car_id},
            "customer": {self.name},
            "car": {self.vehicle},
            "rental_data": {self.rental_date},
            "return_date": datetime.now(),
            "total_days": {self.days},
            "total_cost": {self.total_cost},

        }

        self.available_cars.append(giveaway["car_id"])
        self.rented_cars.remove(giveaway["car_id"])
        self.save_to_file(self.available_cars, "available_cars.txt")
        self.save_to_file(self.rented_cars, "rented_cars.txt")
        return giveaway

