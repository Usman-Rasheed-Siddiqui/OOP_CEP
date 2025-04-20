
from user import User

class Customer(User):
    def __init__(self, first_name, last_name, user_id, email, phone_number, license_card_number):
        User.__init__(self, first_name, last_name, user_id, email, phone_number)
        self.license_card_number = license_card_number
        self.rental_history = []

    def add_rental_record(self):
        """Adds a new record of rental from the User"""
        record = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'user_id': self.user_id,
            'email': self.email,
            'phone_number': self.phone_number,
            'license_card_number': self.license_card_number,
        }
        self.rental_history.append(record)
        return record


    def rent_vehicle(self, vehicle, rental_manager):
        """Use to rent a vehicle"""
        return rental_manager.rent_vehicle(self, vehicle)

    def return_vehicle(self, uuid, rental_manager):
        """Use to return the rented vehicle"""
        return rental_manager.return_vehicle(self, uuid)

    def show_available_cars(self, rental_manager):
        """Displays all available cars"""
        available_cars = rental_manager.get_available_cars()

        if not available_cars:
            print("No available cars right now")
            return

        print("\n=== CARS AVAILABLE TO RENT===")
        for i, car in enumerate(available_cars, 1):
            print(f"{i}. {car.brand} {car.model} - {car.price_per_day} PKR/day")
            print("============================")
            