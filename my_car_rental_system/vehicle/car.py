from .vehicle import Vehicle
from file_handler.file_handler import FileHandler
from exception_handling.Exceptions import CarNotAvailableError

class Car(Vehicle):
    """A car which sets information for a specific vehicle. It is the child class of 'Vehicle'.
    Attributes: car_id, brand, model, seating_capacity, price_per_day, fuel_type, car_type,
    fuel_average,availability
    Methods: display_vehicle_info(), rental_history() """
    def __init__(
            self,
            brand="",
            model="", seating_capacity="",
            price_per_day="", fuel_type="", car_type="",
            fuel_average="",availability=True,
    ):

        super().__init__(brand, model, seating_capacity, price_per_day, availability)
        self.fuel_type = fuel_type
        self.fuel_average = fuel_average
        self.car_type = car_type



    def display_vehicle_info(self):
        file_handler = FileHandler()
        data = file_handler.load_from_file("cars.txt")

        while True:
            try:
                print("Enter q/Q to exit ")
                brand = input("Brand name (example: Toyota): ").strip()
                if brand == "q" or brand == "Q":
                    return
                model = input("Model name (example: Corolla): ").strip()
                if model == "q" or model == "Q":
                    return
                if not brand or not model:
                    raise TypeError("Brand or model not found.")

                car_found = False
                count = 0
                for car in data:
                    if car["brand"].lower() == brand.lower() and car["model"].lower() == model.lower() and car["availability"] == True:
                        count += 1
                        car_found = True
                        brand = car["brand"]
                        model = car["model"]
                        type = car["car_type"]
                        price_per_day = car["price_per_day"]
                        seating_capacity = car["seating_capacity"]
                        fuel_type = car["fuel_type"]
                        fuel_average = car["fuel_average"]
                if not car_found:
                    raise CarNotAvailableError

                print(f"""
{"=" * 25}    
    CAR INFORMATION
{"=" * 25}
Car : {brand} {model}
Car Type: {type}
{"=" * 25}
Seating Capacity : {seating_capacity}
Price/Day : {price_per_day} PKR
Fuel Type : {fuel_type}
Fuel Average : {fuel_average}
Available Cars : {count}
{"=" * 25}""")
                return True

            except CarNotAvailableError as e:
                print("Error:",e)


