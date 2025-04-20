
from user import User

class Admin(User):
    def __init__(self, first_name, last_name, user_id, email, phone_number, admin):
        super().__init__(first_name, last_name, user_id, email, phone_number)
        self.admin = admin

    def add_vehicle(self, vehicle, inventory):
        """Adds a new vehicle to the inventory"""
        inventory.append(vehicle)

    def remove_vehicle(self, vehicle, uuid, inventory):
        """Removes a vehicle from the inventory"""
        for vehicle in inventory:
            if vehicle.id == uuid:
                inventory.remove(vehicle)
                return f"Vehicle {vehicle.brand} {vehicle.model} was removed successfully"
        return f"Vehicle {vehicle.brand} {vehicle.model} was not removed"


