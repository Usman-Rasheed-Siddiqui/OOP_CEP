
from datetime import datetime

class RentalManager():
    """A class that manages the renting of a vehicle. When that vehicle is being returned and whether
    that vehicle is available or not during rental process"""

    def __init__(self):
        self.active_rental_list = []
        self.available_vehicles = []
        self.rented_vehicles = []

    def process_rental(self, vehicle, customer, days):
        """For processing information regarding the rental from customer"""
        if not vehicle.available:
            raise Exception("Vehicle is not available")

        rental = {
            "customer": customer,
            "vehicle": vehicle,
            "rental_date": datetime.now(),
            "returned_date": None,
            "expected_days": days,
            "total_rent": vehicle.price_per_day * days
        }

        self.active_rental_list.append(rental)
        vehicle.available = False
        return rental

    def process_return(self, uuid):
        """For processing information regarding the return from customer"""
        for rental in self.active_rental_list:
            #Calculating Final Cost
            if rental["vehicle"].uuid == uuid and not rental["returned_date"]:
                rental["returned_date"] = datetime.now()
                actual_days = (datetime.now() - rental["rental_date"]).days
                final_cost = rental['vehicle'].price_per_day * actual_days

            # Update History
            rental_history = {
                'car': f"{rental['vehicle'].brand} {rental['vehicle'].model}",
                'rental_date': rental['rental_date'],
                'returned_date': rental['returned_date'],
                'days': actual_days,
                'total_rent': rental['total_rent'],
            }
            rental['customer'].rental_history.append(rental_history)

            #Making car available again
            rental['vehicle'].available = True
            self.active_rental_list.remove(rental)

            return final_cost
        return Exception("Return process did not complete")

    def get_vehicle(self, uuid):
        """For renting the vehicle to the customer"""
        for vehicle in self.available_vehicles + self.rented_vehicles:
            if vehicle.uuid == uuid:
                return vehicle
        raise ValueError(f"Vehicle with UUID: '{uuid}' not found")

    def get_available_vehicles(self):
        """For getting every available vehicle to be rented"""
        return [car for car in self.available_vehicles if car.available]


