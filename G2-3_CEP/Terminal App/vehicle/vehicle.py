# Import required modules and classes
from abc import ABC, abstractmethod  # For creating abstract base classes
import uuid  # For generating unique car IDs
from file_handler.file_handler import FileHandler  # For file operations
import time  # For adding delays in the interface


class Vehicle(ABC, FileHandler):
    """
    Abstract base class representing a vehicle in the rental system.
    Serves as the foundation for all specific vehicle types (like Car).
    Inherits from ABC (Abstract Base Class) and FileHandler for file operations.

    Attributes:
        car_id (UUID): Unique identifier for the vehicle
        brand (str): Manufacturer name (e.g., "Toyota")
        model (str): Model name (e.g., "Corolla")
        seating_capacity (int/str): Number of seats
        price_per_day (float/int): Daily rental price
        availability (bool): Whether vehicle is available for rent
        bold_italics (str): ANSI escape codes for bold/italic text
        reset (str): ANSI escape code to reset text formatting
    """

    def __init__(self, brand="", model="", seating_capacity="", availability=True, price_per_day=0):
        """
        Initialize a Vehicle instance with basic properties.
        """

        # Generate a unique ID for each vehicle
        self.car_id = uuid.uuid4()
        # Basic vehicle properties
        self.brand = brand
        self.model = model
        self.seating_capacity = seating_capacity
        self.price_per_day = price_per_day
        self.availability = availability
        # ANSI escape codes for text formatting
        self.bold_italics = '\033[1m\033[3m'  # Bold and italic
        self.reset = '\033[0m'  # Reset formatting

    @abstractmethod
    def display_vehicle_info(self):
        """
        Abstract method that must be implemented by child classes.
        Should display detailed information about a specific vehicle.
        """
        pass

    @staticmethod
    def enter_to_continue():
        """
        Pause execution until user presses Enter.
        Prevents the screen from clearing too quickly.
        """
        while input("Press Enter to continue...") != "":
            print("Please just press Enter without typing anything.")

    def quit_choice(self, choice):
        """
        Check if user wants to quit/return to menu.

        Args:
            choice (str): User's input to check

        Returns:
            bool: True if user wants to quit, False otherwise
        """
        if choice == "q" or choice == "Q":
            print("Returning back to menu.....\n")
            time.sleep(0.5)  # Small delay for better UX
            return True
        return False

    def display_all_vehicles(self):
        """
        Display all available vehicles in a formatted table.
        Shows complete inventory of rentable vehicles.
        """
        # Print table header
        print("=" * 105)
        print("                                         ALL AVAILABLE VEHICLES")
        print("=" * 105)
        print()

        # Load vehicle data from file
        file_handler = FileHandler()
        cars = file_handler.load_from_file("cars.txt")

        # Check if any vehicles exist in system
        if not cars:
            print("No cars available right now.")
            self.enter_to_continue()
            print("Returning back to menu.....\n")
            time.sleep(0.5)
            return

        # Filter for only available vehicles
        true_cars = [car for car in cars if car["availability"]]
        if not true_cars:
            print("No cars available right now.")
            self.enter_to_continue()
            print("Returning back to menu.....\n")
            time.sleep(0.5)
            return

        # Load available cars data
        available_cars = file_handler.load_from_file("available_cars.txt")
        if not available_cars:
            print("No cars available right now.")
            self.enter_to_continue()
            print("Returning back to menu.....\n")
            time.sleep(0.5)
            return

        # Define table columns with their display widths
        columns = [
            ("S.No.", 5), ("Brand", 20), ("Model", 15), ("Seats", 8),
            ("Price/Day (PKR)", 15), ("Type", 10), ("Fuel", 10),
            ("Average", 10), ("Available", 12)
        ]

        # Count availability of each vehicle model
        available_count = {}
        unique_cars = {}
        for car in cars:
            if car["availability"]:
                key = (car["brand"], car["model"])
                if key in available_count:
                    available_count[key] += 1  # Increment count for this model
                else:
                    available_count[key] = 1  # Initialize count
                    unique_cars[key] = car  # Store first instance of this model

        # Generate and print table header
        header = ""
        for col_name, width in columns:
            header += f"| {self.bold_italics}{col_name:<{width}}{self.reset}"
        print(header + "|")

        # Display each unique vehicle model in the table
        for num, (key, car) in enumerate(unique_cars.items(), start=1):
            row = f"| {num:>{columns[0][1]}}"  # Sequence number
            row += f"| {car['brand']:<{columns[1][1]}}"  # Brand name
            row += f"| {car['model']:<{columns[2][1]}}"  # Model name
            row += f"| {car['seating_capacity']:<{columns[3][1]}}"  # Seats
            row += f"| {car['price_per_day']:<{columns[4][1]}}"  # Price
            row += f"| {car['car_type']:<{columns[5][1]}}"  # Vehicle type
            row += f"| {car['fuel_type']:<{columns[6][1]}}"  # Fuel type
            row += f"| {car['fuel_average']:<{columns[7][1]}}"  # Fuel efficiency
            row += f"| {available_count[key]:<{columns[8][1]}}"  # Available count
            print(row + "|")

        # Wait for user before returning to menu
        self.enter_to_continue()
        print("Returning back to user menu....")
        time.sleep(0.5)

    def display_available_cars_names(self):
        """
        Display a simplified list of available car models.
        Shows just brand, model, price and availability count.
        """
        print("AVAILABLE CARS")
        print("Please write brand and model of car from the given list:")
        print()

        # Load car data from file
        file_handler = FileHandler()
        cars = file_handler.load_from_file("cars.txt")

        # Define table columns with widths
        columns = [
            ("S.No.", 5), ("Brand", 20), ("Model", 15),
            ("Price/Day (PKR)", 15), ("Available", 12)
        ]

        # Count availability of each model
        available_count = {}
        unique_cars = {}
        for car in cars:
            if car["availability"]:
                key = (car["brand"], car["model"])
                if key in available_count:
                    available_count[key] += 1  # Increment count
                else:
                    available_count[key] = 1  # Initialize count
                    unique_cars[key] = car  # Store first instance

        # Generate and print table header
        header = ""
        for col_name, width in columns:
            header += f"| {self.bold_italics}{col_name:<{width}}{self.reset}"
        print(header + "|")

        # Display each unique model in the table
        for num, (key, car) in enumerate(unique_cars.items(), start=1):
            row = f"| {num:>{columns[0][1]}}"  # Sequence number
            row += f"| {car['brand']:<{columns[1][1]}}"  # Brand
            row += f"| {car['model']:<{columns[2][1]}}"  # Model
            row += f"| {car['price_per_day']:<{columns[3][1]}}"  # Price
            row += f"| {available_count[key]:<{columns[4][1]}}"  # Available count
            print(row + "|")