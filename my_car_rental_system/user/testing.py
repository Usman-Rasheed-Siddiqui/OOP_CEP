from file_handler.file_handler import FileHandler
from rental_management.rental_manager import RentalManager
from exception_handling.Exceptions import AlreadyRentedError

class Testing:
    def __init__(self, first_name="", last_name="", password="", address="", balance=0):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.address = address
        self.balance = balance
        self.rented_cars = 0
        self.name = self.first_name + " " + self.last_name

    def check_rent(self, rented_car):
        if rented_car == 1:
            raise AlreadyRentedError("You already have a car rented")

    def renting(self, brand, model, customer):
        file_handler = FileHandler()

        users = file_handler.load_from_file("users.txt")
        try:
            for user in users:
                if user["name"] == customer:
                    self.check_rent(user["rented_car"])

        except AlreadyRentedError as e:
            print(f"Error: {e}")
            return

        safe_name = customer.replace(" ", "_")
        user_rental_history = file_handler.load_from_file(f"users/{safe_name}.txt")

        rental_manager = RentalManager(brand, model)
        car = rental_manager.process_rental(customer)
        if not car:
            return

        rent = {
                "car_id" : car["car_id"],
                "brand" : car["brand"],
                "model" : car["model"],
                "days" : rental_manager.days,
                "rental_date" : rental_manager.rental_date.strftime("%Y-%m-%d"),
                "return_date" : rental_manager.return_date.strftime("%Y-%m-%d"),
                "total_cost" : rental_manager.total_cost,
                }

        for user in users:
            if user["name"] == customer:
                user["rented_car"] = 1

                user_rental_history.append(rent)
                file_handler.save_to_file(users, "users.txt")
                file_handler.save_to_file(user_rental_history, f"users/{safe_name}.txt")
                break

T1 = Testing()
T1.renting("toyota", "corolla", "Usman Siddiqui")


