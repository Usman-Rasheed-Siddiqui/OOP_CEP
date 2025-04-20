
from .vehicle import Vehicle

class Car(Vehicle):

    def __init__(self, brand, model, seating_capacity, price_per_day, no_of_cars, car_type, fuel_type, available=True):
        super().__init__(brand, model, seating_capacity, price_per_day, no_of_cars, available)
        self.car_type = car_type
        self.fuel_type = fuel_type

    def display_info(self):
        return f'''
{"="*35}
UUID No.: {self.uuid}
{self.brand} {self.model} ({self.car_type})
{"="*35}
Seating Capacity: {self.seating_capacity}
Price Per Day: {self.price_per_day} PKR
Car Type: {self.car_type}
Fuel Type: {self.fuel_type}
Availability: {"Available" if self.available else "Not Available"}
{"="*35}
'''
