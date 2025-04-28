from user.customer import Customer
from user.admin import Admin

class Frontend:
    def __init__(self):
        self.main_menu()

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
            self.name = input("\nEnter your name: ")
            password = input("\nEnter your password: ")

            customer = Customer(first_name=None, last_name=None, password=None, address=None, balance=None)
            customer.password_check(self.name, password, self.customer_main_menu())

        if choice == 2:
            name = input("\nEnter your name: ")
            lst = name.split(" ")
            password = input("\nEnter your password: ")
            admin = Admin(lst[0], lst[1], password)
            admin.check_admin_password(name, password, self.admin_main_menu())

        if choice == 3:
            first_name = input("\nEnter First name: ")
            last_name = input("\nEnter Last name: ")
            password = input("\nEnter Password: ")
            address = input("\nEnter Address: ")
            balance = input(int("\nEnter Balance: "))

            customer = Customer(first_name, last_name, password, address, balance)
            customer.create_an_account(first_name, last_name, password, address, balance)
            print('\nYour account has been created.')

        if choice == 4:
            print("Thank you for using our Car Rental System!")
            exit()

    def customer_main_menu(self):
        print("\nRent a Car")
        print("\n1. Return a Car")
        choice = int(input("\nChoose an option: "))

        if choice == 1:
            print("\nCAR RENTING")
            brand = input("\nEnter brand: ")
            model = input("\nEnter model: ")
            days = input("\nEnter days: ")
            customer = Customer(None, None, None, None, None)
            customer.renting(brand, model, days)

        if choice == 2:
            print("\nCAR RETURNING")
            car_id = input("\nEnter your car id: ")
            customer = Customer(None, None, None, None, None)
            customer.returning(self.name, car_id)

    def admin_main_menu(self):
        print("\n1. Add a Car")
        print("\n2. Remove a Car")
        print("\n3. Print Customers' Report")
        print("\n4. Access Feedbacks")
        choice = int(input("\nChoose an option: "))
        admin = Admin(None, None, None)

        if choice == 1:
            print("\nADDING A CAR")
            brand = input("\nEnter brand name: ")
            model = input("\nEnter model name: ")
            seating_capacity = input("\nEnter seating capacity: ")
            price_per_day = input("\nEnter price per day: ")
            fuel_type = input("\nEnter fuel type: ")
            car_type = input("\nEnter car type: ")
            fuel_average = input("\nEnter fuel average: ")

            admin.add_a_new_car(brand, model, seating_capacity, price_per_day, fuel_type, car_type,
            fuel_average, availability=True)


        if choice == 2:
            print("\nREMOVING A CAR")
            brand = input("\nEnter brand name: ")
            model = input("\nEnter model name: ")

            admin.remove_car(brand, model)

        if choice == 3:
            print("\nPRINTING CUSTOMER REPORTS")
            admin.print_customers_report()

        if choice == 4:
            print("\nACCESSING FEEDBACKS")
            admin.access_feedbacks()

