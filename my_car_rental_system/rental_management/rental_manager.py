from datetime import datetime
from file_handler.file_handler import FileHandler

class RentalManager:
    def __init__(self, brand="", model="", car_id="", expected_cost=0):

        self.brand = brand
        self.model = model
        self.car_id = car_id
        self.rental_date = None
        self.return_date = None
        self.days = int(input("Enter the number of days: "))
        self.expected_cost = expected_cost
        self.final_cost = None
        self.file_handler = FileHandler()

        self.available_cars =self.file_handler.load_from_file("available_cars.txt")
        self.rented_cars = self.file_handler.load_from_file("rented_cars.txt")




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

    def process_rental(self, customer):
        for car in self.available_cars:
            if car["brand"] == self.brand and car["model"] == self.model:
                self.expected_cost = self.days * int(car["price_per_day"])
                self.car_id = car["car_id"]
                break

        self.rental_date = datetime.now()

        rental = {
            "car_id": self.car_id,
            "customer": customer,
            "brand": self.brand,
            "model": self.model,
            "rental_data": str(self.rental_date),
            "return_date": str(self.return_date),
            "total_days": self.days,
            "total_cost": self.expected_cost,
        }

        self.rented_cars.append(rental)

        for car in self.available_cars:
            if car["car_id"] == rental["car_id"]:
                self.available_cars.remove(car)
                break

        self.file_handler.save_to_file(self.available_cars, "available_cars.txt")
        self.file_handler.save_to_file(self.rented_cars, "rented_cars.txt")

        return rental

    def process_return(self, car_id, customer):

        self.return_date = datetime.now()
        self.days = self.return_date - self.rental_date

        giveaway = {
            "car_id": {car_id},
            "customer": {customer},
            "brand": {self.brand},
            "model": {self.model},
            "rental_data": {self.rental_date},
            "return_date": {self.return_date},
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

    def print_receipt(self, first_name, last_name):
        return f"""
{"="*30}
    RECEIPT
{"="*30}
Customer Name : {first_name} {last_name}
Car ID: {self.car_id}
Car : {self.brand} {self.model}
Rental Date : {self.rental_date}
Expected Days : {self.days}
{"="*30}
Expected Cost: {self.expected_cost}
{"="*30}
"""

rental_manager = RentalManager("Toyota", "Corolla")
rental_manager.process_rental("Usman Siddiqui")
