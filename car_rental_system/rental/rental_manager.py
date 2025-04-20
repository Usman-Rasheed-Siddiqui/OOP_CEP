
from datetime import datetime
from rental import Rental
from car_rental_system.filehandler import FileHandler
from car_rental_system.vehicles.vehicle import Vehicle

class RentalManager():
    """A class that manages the renting of a vehicle. When that vehicle is being returned and whether
    that vehicle is available or not during rental process"""

    def __init__(self):
        self.active_rental_list = FileHandler.load_from_file(Rental, "data/rentals.txt")
        self.available_vehicles = [vehicle for vehicle in FileHandler.load_from_file(Vehicle, "data/cars.txt") if vehicle.available]
        self.rented_vehicles = [vehicle for vehicle in FileHandler.load_from_file(Vehicle, "data/cars.txt") if not vehicle.available]

    def process_rental(self, vehicle, customer, days):
        """For processing information regarding the rental from customer"""
        if not vehicle.available:
            raise Exception("Vehicle is not available for rental")

        rental = Rental(vehicle, customer, days)
        self.active_rental_list.append(rental)
        vehicle.available = False
        FileHandler.save_to_file(self.active_rental_list, "data/rentals.txt")
        FileHandler.save_to_file(self.available_vehicles + self.rented_vehicles, "data/cars.txt")

        return rental

    def process_return(self, uuid):
        """For processing information regarding the return from customer"""
        for rental in self.active_rental_list:
            #Calculating Final Cost
            if rental.vehicle.uuid == uuid and not rental.return_date:
                rental.return_date = datetime.now()
                rental.vehicle.available = True

                self.rented_vehicles.remove(rental.vehicle)
                self.available_vehicles.append(rental.vehicle)
                FileHandler.save_to_file(self.active_rental_list, "data/rentals.txt")
                FileHandler.save_to_file(self.available_vehicles + self.rented_vehicles, "data/cars.txt")
                return rental

        raise Exception("No active rental detected for vehicle with this uuid")


    def get_vehicle(self, uuid):
        """For renting the vehicle to the customer"""
        for vehicle in self.available_vehicles:
            if vehicle.uuid == uuid:
                return vehicle
        raise ValueError(f"Vehicle with UUID: '{uuid}' not found")

    def get_available_vehicles(self):
        """For getting every available vehicle to be rented"""
        return [car for car in self.available_vehicles if car.available]
