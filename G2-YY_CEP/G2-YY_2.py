
import os

class Cars:
    '''A Class of Cars Used to check on the number of cars available for rent and their brand, models
    and seating capacity.'''
    def __init__(self, brand="", model="", seating_capacity=0, price_per_day=0,no_of_cars=0, available=False):
        self.brand = brand
        self.seating_capacity = seating_capacity
        self.model = model
        self.price_per_day = price_per_day
        self.no_of_cars = no_of_cars
        self.available = available


    def display_available_cars(self):
        pass

    def display_car_info(self):
        '''To read the information of the car'''
        self.get_file_name()
        self.set_car_info()

        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as file:
                content = file.read()
                return content
        else:
            return f"Car not found"

    def get_file_name(self):
        self.file_name = f"Car/{self.brand}_{self.model}.txt"

    def set_car_info(self):
        self.car_info = f'''
                ================================
                        CAR INFORMATION
                ================================
                Car Name: {self.brand}
                Model Name: {self.model}
                Seating Capacity: {self.seating_capacity}
                Price Per Day: {self.price_per_day}
                No of Cars: {self.no_of_cars}
                Avalaibility: {"Available" if self.available else "Not Available"}
                '''
    def get_car_info(self):
        return self.car_info


    def rent_car(self):
        '''To update the rent record of a car'''
        if self.available:
            self.available = False
            return True
        return False

    def return_car(self):
        '''To update the rent record of a car'''
        self.available = True

    def __str__(self):
        return f"{self.display_car_info() if self.available else "Car not Available"}"

class Administrator(Cars):

    def __init__(self):
        Cars.__init__(self,  brand="", model="", seating_capacity=0, price_per_day=0, no_of_cars=0, available=True)

    def update_car(self):
        '''To Update or Add the record of car'''
        Cars.get_file_name(self)
        Cars.get_car_info(self)
        with open(self.file_name, "w") as file:
            file.write(self.car_info.strip())
        print(f"{self.brand} {self.model} information saved successfully")

    def add_car(self):
        '''Enter information of a car to be added'''
        self.brand = input("Enter Brand Name: ")
        self.model = input("Enter Model Name: ")
        self.cars.append({self.brand, self.model})
        self.seating_capacity = int(input("Enter Seating Capacity: "))
        self.price_per_day = int(input("Enter Price Per Day: "))
        self.available = True
        self.update_car()

C1 = Cars(input("Enter Brand Name: "), input("Enter Model Name: "), int(input("Enter Seating Capacity: ")),
              int(input("Enter Price Per Day: ")), int(input("Enter No of Cars: ")), input("Enter Availability (True/False): ").strip().lower() == "true")
C1.set_car_info()
print(C1.display_car_info())