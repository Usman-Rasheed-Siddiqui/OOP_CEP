from vehicle import Vehicle

class Car(Vehicle):
    """A car which sets information for a specific vehicle. It is the child class of 'Vehicle'.
    Attributes: car_id, brand, model, seating_capacity, price_per_day, fuel_type, car_type,
    fuel_average,availability
    Methods: display_vehicle_info(), rental_history() """
    def __init__(
            self,
            brand,
            model, seating_capacity,
            price_per_day, fuel_type, car_type,
            fuel_average,availability=True
    ):

        super().__init__(brand, model, seating_capacity, price_per_day, availability)
        self.fuel_type = fuel_type
        self.fuel_average = fuel_average
        self.car_type = car_type
        self.rental_history = []

    def display_vehicle_info(self):

        return f"""
{"="*30}
        CAR INFORMATION
{"="*30}
Car ID : {self.car_id}
Car : {self.brand} {self.model}
Car Type: {self.car_type}
{"="*30}
Seating Capacity : {self.seating_capacity}
Price/Day : {self.price_per_day}
Fuel Type : {self.fuel_type}
Fuel Average : {self.fuel_average}
Availability : {"Available" if self.availability else "Not Available"}
{"="*30}
"""

    def save_rental_history(self):
        """For saving a vehicle's rental history"""
        history = {
            "Renting Date": {self.},
            "Return Date": {self.},
            "Days": {self.},
            "Total Cost": {self.},
        }                           # Needs attributes from Rentals
        self.rental_history.append(history)
        return history

    def print_rental_history(self):
        """Printing the rental history"""
        for num,rents in enumerate(self.rental_history):
            print(f"{num}.",end=" ")
            for att, specification in rents.items():
                print(f"{att} : {rents}", end =" | ")