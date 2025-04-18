
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
        self.car_info = (
                "================================\n"
                "       CAR INFORMATION\n"
                "================================\n"
                f"Car Name: {self.brand}\n"
                f"Model Name: {self.model}\n"
                f"Seating Capacity: {self.seating_capacity}\n"
                f"Price Per Day: {self.price_per_day}\n"
                f"No of Cars: {self.no_of_cars}\n"
                f"Availability: {"Available" if self.available else "Not Available"}\n"
        )
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
        super().__init__()
        self.cars = []

    def update_car(self):
        '''To Update or Add the record of car'''
        self.set_car_info()
        file_name = self.get_file_name()
        
        os.makedirs("Car", exist_ok=True)
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
        self.no_of_cars = int(input("Enter No of Cars: "))
        self.available = True

        car = Cars(self.brand, self.model, self.seating_capacity, self.price_per_day, self.no_of_cars, self.available)
        self.cars.append(car)
        print(f"{self.brand}_{self.model} added successfully")
        self.set_car_info()
        with open(f"Car/{self.brand}_{self.model}.txt", "w") as car_file:
            car_file.write(self.get_car_info())

    def show_car(self):
        '''To Check information of a car'''
        if not self.cars:
            print("No Cars Available")
        else:
            for car in self.cars:
                print(car.display_car_info())

admin = Administrator()
admin.add_car()
print(admin.display_car_info())