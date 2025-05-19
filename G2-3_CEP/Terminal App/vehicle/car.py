# Import required modules and classes
from .vehicle import Vehicle  # Import base Vehicle class that Car inherits from
from file_handler.file_handler import FileHandler  # For reading/writing car data to files
from exception_handling.CustomExceptions import CarNotAvailableError  # Custom error when car isn't available
import time  # For adding small delays in the user interface


class Car(Vehicle):
    """
    Represents a car in the rental system with all its properties and behaviors.
    Inherits basic vehicle attributes and methods from the Vehicle parent class.
    Adds car-specific features like fuel type and efficiency.

    Attributes (inherited from Vehicle plus these additional ones):
        fuel_type (str): The type of fuel the car uses (e.g., petrol, diesel, electric)
        fuel_average (str): The car's fuel efficiency (e.g., '15 km/l')
        car_type (str): The category of car (e.g., sedan, SUV, hatchback)
    """

    def __init__(
            self,
            brand="",
            model="",
            seating_capacity="",
            price_per_day="",
            fuel_type="",
            car_type="",
            fuel_average="",
            availability=True,
    ):
        """
        Constructor method to initialize a new Car instance with provided details.
        Sets up both the inherited Vehicle attributes and car-specific attributes.
        """
        # Initialize parent Vehicle class attributes
        super().__init__(brand, model, seating_capacity, price_per_day, availability)

        # Initialize car-specific attributes
        self.fuel_type = fuel_type  # e.g., "Petrol", "Diesel", "Electric"
        self.fuel_average = fuel_average  # e.g., "15 km/l"
        self.car_type = car_type  # e.g., "Sedan", "SUV", "Hatchback"


    def display_vehicle_info(self):
        """
        Displays detailed information about a specific available car that the user selects.
        Shows a formatted display of all car properties after user provides brand and model.
        """
        # Print header for the vehicle display section
        print("=" * 68)
        print("                       ALL AVAILABLE VEHICLES")
        print("=" * 68)
        print()

        # Create file handler instance to load car data
        file_handler = FileHandler()

        # Load all car records from the data file
        data = file_handler.load_from_file("cars.txt")
        cars = file_handler.load_from_file("cars.txt")

        # Check if any cars exist in the system at all
        if not cars:
            print("No cars available right now.")
            self.enter_to_continue()  # Wait for user to press enter
            print("Returning back to menu.....\n")
            time.sleep(0.5)  # Small delay for better UX
            return

        # Filter the cars list to only include available cars (availability=True)
        true_cars = [car for car in cars if car["availability"]]

        # Check if any available cars exist after filtering
        if not true_cars:
            print("No cars available right now.")
            self.enter_to_continue()
            print("Returning back to menu.....\n")
            time.sleep(0.5)
            return

        # Load the separate available cars file
        available_cars = file_handler.load_from_file("available_cars.txt")
        if not available_cars:
            print("No Cars Available Right Now")
            self.enter_to_continue()
            print("Returning back to user menu.....\n")
            time.sleep(0.5)
            return

        # Display available cars section header
        print("AVAILABLE CARS")
        print("Please type brand and model name from any of the following to view it.")

        # Show just the names of available cars for user to choose from
        self.display_available_cars_names()
        print()

        # Main input loop for selecting a specific car
        while True:
            try:
                # Prompt for brand name with option to quit
                print("Enter q/Q to exit ")
                brand = input("Brand name (example: Toyota): ").strip()

                # Check if user wants to quit (entered q/Q)
                if self.quit_choice(brand):
                    return

                # Prompt for model name
                model = input("Model name (example: Corolla): ").strip()
                if self.quit_choice(model):
                    return

                # Validate that both fields were provided
                if not brand or not model:
                    raise TypeError("Please enter Brand/Model name.")

                # Search through all cars for matching brand/model
                car_found = False
                count = 0
                for car in data:
                    # Case-insensitive comparison of brand and model
                    if (car["brand"].lower() == brand.lower() and
                            car["model"].lower() == model.lower() and
                            car["availability"] == True):
                        count += 1
                        car_found = True

                        # Store matching car's details
                        brand = car["brand"]
                        model = car["model"]
                        type = car["car_type"]
                        price_per_day = car["price_per_day"]
                        seating_capacity = car["seating_capacity"]
                        fuel_type = car["fuel_type"]
                        fuel_average = car["fuel_average"]

                # If no matching available car found, raise error
                if not car_found:
                    raise CarNotAvailableError

                # Display the car information in a formatted box
                print(f"""
{"=" * 30}    
        CAR INFORMATION
{"=" * 30}
{self.bold_italics}Car{self.reset} : {brand} {model}
{self.bold_italics}Car Type: {type}
{"=" * 30}
{self.bold_italics}Seating Capacity{self.reset} : {seating_capacity}
{self.bold_italics}Price/Day{self.reset} : {price_per_day} PKR
{self.bold_italics}Fuel Type{self.reset} : {fuel_type}
{self.bold_italics}Fuel Average{self.reset} : {fuel_average}
{self.bold_italics}Available Cars{self.reset} : {count}
{"=" * 30}""")

                # Wait for user to acknowledge before continuing
                self.enter_to_continue()
                print("Returning back to user menu....")
                time.sleep(0.5)
                return True

            # Handle specific exceptions with error messages
            except CarNotAvailableError as e:
                print("Error:", e)
            except TypeError as e:
                print("Error:", e)

    def cars_rental_history(self):
        """
        Displays the complete rental history for a specific car model.
        Shows past rental records including rental dates, return dates, and car IDs.
        """
        # Print header for rental history section
        print("=" * 68)
        print("                         CARS RENTAL HISTORY")
        print("=" * 68)
        print()
        print("Press q/Q at anytime to quit")
        print()

        # Create file handler and load rental history data
        file_handler = FileHandler()
        rental_history = file_handler.load_from_file("cars_rental_history.txt")
        cars = file_handler.load_from_file("cars.txt")

        # Check if any rental history exists at all
        if not rental_history:
            print("No cars rental history available.")
            self.enter_to_continue()
            print("Returning back to menu.....\n")
            time.sleep(0.5)
            return

        # Initialize list to store filtered history records
        car_history = []

        # Show available car names for reference
        self.display_available_cars_names()
        print()

        # Flag variables for input validation
        brand_found = False
        model_found = False

        # Brand input loop with validation
        while True:
            try:
                brand = input("Brand name (example: Toyota): ").strip()

                # Check for quit command
                if self.quit_choice(brand):
                    return

                # Validate brand input
                if not brand:
                    raise TypeError("Please enter Brand name.")
                if brand.isdigit():
                    raise ValueError("Please enter Brand name.")

                # Check if brand exists in system
                for car in cars:
                    if car["brand"].lower() == brand.lower():
                        brand_found = True
                        self.brand = car["brand"]

                if not brand_found:
                    raise Exception("No Car with this brand name found.")

                break  # Exit loop if valid brand found

            # Handle various input errors
            except TypeError as e:
                print("Error:", e)
            except ValueError as e:
                print("Error:", e)
            except Exception as e:
                print("Error:", e)

        # Model input loop with validation
        while True:
            try:
                model = input("Model name (example: Corolla): ").strip()
                if self.quit_choice(model):
                    return

                # Validate model input
                if not model:
                    raise TypeError("Please enter Model name.")
                if model.isdigit():
                    raise ValueError("Please enter Model name.")

                # Check if model exists for selected brand
                for car in cars:
                    if (car["model"].lower() == model.lower() and
                            car["brand"].lower() == brand.lower()):
                        model_found = True
                        self.model = car["model"]

                if not model_found:
                    raise Exception("No Car with this brand and model name found.")

                break  # Exit loop if valid model found

            # Handle input errors
            except TypeError as e:
                print("Error:", e)
            except ValueError as e:
                print("Error:", e)
            except Exception as e:
                print("Error:", e)

        # Filter rental history for selected car
        while True:
            try:
                # Find all history records matching brand and model
                for car in rental_history:
                    if (car["brand"].lower() == self.brand.lower() and
                            car["model"].lower() == self.model.lower()):
                        car_history.append(car)

                # If no history found for this car
                if not car_history:
                    raise Exception("No rental history found for this car. Please try again later.")
                break

            except Exception as e:
                print("Error:", e)
                self.enter_to_continue()
                print("Returning back to user menu....")
                time.sleep(0.5)
                return

        # Define table columns for display with their widths
        columns = [
            ("S.No.", 5),  # Sequence number
            ("Car ID", 40),  # Unique car identifier
            ("Rental Date", 15),  # Date car was rented
            ("Return Date", 15)  # Date car was returned
        ]

        # Print spacing and car name header
        print("\n\n\n")
        print(f"{self.bold_italics}Car Name:{self.reset} {self.brand} {self.model}")

        # Generate and print table header
        header = ""
        for col_name, width in columns:
            header += f"| {self.bold_italics}{col_name:<{width}}{self.reset}"
        print(header + "|")

        # Print each rental record in the table
        for num, rental in enumerate(car_history, start=1):
            row = f"| {num:<{columns[0][1]}}"  # Sequence number
            row += f"| {rental['car_id']:<{columns[1][1]}}"  # Car ID
            row += f"| {rental['rental_date']:<{columns[2][1]}}"  # Rental date
            row += f"| {rental['return_date']:<{columns[3][1]}}"  # Return date
            print(row + "|")

        # Final spacing and return to menu
        print()
        self.enter_to_continue()
        print("Returning back to user menu....")
        time.sleep(0.5)
        return