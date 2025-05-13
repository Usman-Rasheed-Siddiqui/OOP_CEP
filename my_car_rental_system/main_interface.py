from users.customer import Customer
from vehicle.car import Car
from users.admin import Admin

class Interface:
    def __init__(self):
        self.admin = Admin()
        self.customer = Customer()
        self.car = Car()

    def quit_choice(self, choice):
        """Check if user wants to quit (entered 'q' or 'Q')"""
        if choice == "q" or choice == "Q":
            return True
        return False

    def main_menu(self):
        """Display main menu and handle choices"""
        print("="*30)
        print("WELCOME TO OUR CAR RENTAL SYSTEM")
        print("="*30)
        self.main_menu_interface()
        self.choice_main()

    def main_menu_interface(self):
        print("Please choose from the following options:")
        print("1. Login")
        print("2. Create new account")
        print("3. Login as an Administrator")
        print("4. Exit")

    def choice_main(self):
        while True:
            choice = input("\nEnter your choice here: ")

            try:
                choice = int(choice)
                if choice == 1:
                    if self.customer.login():
                        self.user_menu()
                        break

                elif choice == 2:
                    self.customer.create_an_account()

                elif choice == 3:
                    self.admin.login()

                elif choice == 4:
                    exit()

                else:
                    raise ValueError

            except TypeError:
                print("Error: You did not enter a number. Please enter a number from 1 ----> 4")

            except ValueError:
                print("Please enter a number from 1 ----> 4")

    def user_menu(self):
        """Display user menu and handle choices"""
        print("=" * 30)
        print(f"\nMr./ Mrs {self.customer.name.upper()}'s Dashboard")
        print("=" * 30)
        self.user_menu_interface()
        self.choice_user()

    def user_menu_interface(self):
        print("=" * 30)
        print(f"Mr./ Mrs {self.customer.name.upper()}'s Dashboard")
        print("=" * 30)
        print("Please choose from the following options:")
        print("1. Rent a Car")
        print("2. Return Car")
        print("3. View All Available Cars")
        print("4. View Specific Car")
        print("5. Exit")
        print()

    def choice_user(self):
        while True:
            try:
                print("Press q/Q to quit to main menu. (You have to then login again)")
                choice = input("\nEnter your choice here: ")

                if self.quit_choice(choice):
                    return self.main_menu()

                if choice == "1":
                    self.customer.renting()

                if choice == "2":
                    self.customer.returning()

                if choice == "3":
                    self.car.display_all_vehicles()

                if choice == "4":
                    self.car.display_vehicle_info()

                if choice == "5":
                    self.main_menu()

                #  EXCEPTION: Invalid entry
                if not choice.isdigit():
                    raise TypeError
                #  EXCEPTION: Invalid number entry
                if int(choice) < 1 or int(choice) > 5:
                    raise ValueError

            #  HANDLING: Invalid entry
            except TypeError:
                print("Error: You did not enter a number. Please enter a number from 1 ----> 5")

            #  HANDLING: Invalid number entry
            except ValueError:
                print("Please enter a number from 1 ----> 5")



