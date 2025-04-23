from rental_management.rental_manager import RentalManager
from vehicle.car import Car
from user.customer import Customer
from user.admin import Admin

class Frontend:

    def main_menu(self):
        print("\nWelcome to our Car Rental System!")
        print("\nLog in or Create an account!")
        print("\n1. Log in as Customer")
        print("\n2. Log in as Administrator")
        print("\n3. Create an account")
        print("\n4. Exit")

    def choose_option_main(self):
        choice = int(input("\nChoose an option: "))
        if choice == 1:
            

        if choice == 3:
            first_name = input("\nEnter First name: ")
            last_name = input("\nEnter Last name: ")
            password = input("\nEnter Password: ")
            address = input("\nEnter Address: ")
            balance = input(int("\nEnter Balance: "))

            customer = Customer(first_name, last_name, password, address, balance)
            customer.create_an_account(first_name, last_name, password, address, balance)
            print('\nYour account has been created.')






