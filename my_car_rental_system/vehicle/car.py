from vehicle import Vehicle
from file_handler.file_handler import FileHandler

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
            i_d = input("Enter the car id (type e to quit): ")
            if i_d == "e":
                break

            elif len(i_d) != 36:
                print("Invalid car id. Enter a valid car id. (36 characters)")
                continue

            try:
                for car in data:
                    if car["car_id"] == i_d and car["availability"]:
                        print(f"""
{"="*45}    
             CAR INFORMATION
{"="*45}
Car ID : {car["car_id"]}
Car : {car["brand"]} {car["model"]}
Car Type: {car["car_type"]}
{"="*45}
Seating Capacity : {car["seating_capacity"]}
Price/Day : {car["price_per_day"]} PKR
Fuel Type : {car["fuel_type"]}
Fuel Average : {car["fuel_average"]}
Availability : {"Available" if car["availability"] else "Not Available"}
{"="*45}
""")

                print("Car with this ID not available.")
            except KeyError as e:
                raise ValueError("Data format error:",e)

C1 = Car()
C1.display_vehicle_info()