
from rental_manager import RentalManager
from users.admin import Admin
from users.customer import Customer
from vehicles.car import Car

class CarRentalSystem:
    def __init__(self):
        self.manager = RentalManager()
        # Adding some testing cars
        self.manager.add_car(Car("Toyota", "Corolla", 5, 4000, "Sedan", "Petrol"))
        self.manager.add_car(Car("Honda", "Civic", 5, 4500, "Sedan", "Hybrid"))
