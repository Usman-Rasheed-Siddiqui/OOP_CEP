from abc import ABC, abstractmethod
import uuid

class Vehicle(ABC):

    def __init__(self, brand, model, seating_capacity, price_per_day, available=True):
        self.uuid = str(uuid.uuid4())
        self.brand = brand
        self.model = model
        self.seating_capacity = seating_capacity
        self.price_per_day = price_per_day
        self.available = available

    @abstractmethod
    def display_info(self):
        """Display all vehicles' information."""
        pass

    def __eq__(self, other):
        """To match same cars' uuid number"""
        return self.uuid == other.uuid

