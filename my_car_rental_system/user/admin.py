from user import User
from file_handler.file_handler import FileHandler
import uuid

class Admin(User):
    def __init__(self, first_name, last_name, password):
        super().__init__(first_name, last_name, password)
        self.file_handler = FileHandler()

    def display_user_info(self):
        pass

    def add_a_new_car(self,brand, model, seating_capacity, price_per_day, fuel_type, car_type,
            fuel_average,availability=True):

        available_cars = self.file_handler.load_from_file("available_cars.txt")
        new_car = {
            "car_id": uuid.uuid4(),
            "brand": brand,
            "model": model,
            "seating_capacity": seating_capacity,
            "price_per_day": price_per_day,
            "car_type": car_type,
            "fuel_type": fuel_type,
            "fuel_average": fuel_average,
            "availability": availability,
        }
        available_cars.append(new_car)
        self.file_handler.save_to_file(available_cars,"available_cars.txt")
        return new_car

    def  remove_car(self, brand, model):
        available_cars = self.file_handler.load_from_file("available_cars.txt")
        for car in available_cars:
            if car["brand"] == brand and car["model"] == model:
                available_cars.remove(car)

        self.file_handler.save_to_file(available_cars,"available_cars.txt")

    def print_customers_report(self):   # Needs Rental Manager to complete
        users = self.file_handler.load_from_file("users.txt")
        for user in users:
            for name, info in user.items():
                print(f"{name}: {info}", end=" | ")

    def access_feedbacks(self):
        feedbacks = self.file_handler.load_from_file("feedbacks.txt")
        for feedback in feedbacks:
            print(f"{feedback["Name"]} : {feedback['Feedback']}")