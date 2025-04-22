from abc import ABC, abstractmethod
import uuid
from file_handler.file_handler import FileHandler

class Vehicle(ABC, FileHandler):
    """A class which sets the root for all the cars in the rental system. It is an abstract class.
    Attributes: car_id, brand, model, seating_capacity, price_per_day, availability
    Methods: display_vehicle_info() {abstract method}, display_all_vehicles()"""
    def __init__(self, brand, model, seating_capacity, price_per_day, availability=True):
        self.car_id = uuid.uuid4()
        self.brand = brand
        self.model = model
        self.seating_capacity = seating_capacity
        self.price_per_day = price_per_day
        self.availability = availability

    @abstractmethod
    def display_vehicle_info(self):
        """To Display a specific vehicle info"""
        pass

    def display_all_vehicles(self):
        """To display info of all vehicles"""
        vehicles = self.load_from_file("cars.txt")
        for num, vehicle in enumerate(vehicles):
            print(f"{num}.", end=" ")
            for name, attribute in vehicle.items():
                print(f"{name} : {attribute}", end = " | ")