from users.customer import Customer
from vehicle.car import Car
from users.admin import Admin
import time

class Interface:
    def __init__(self):
        self.admin = Admin()
        self.customer = Customer()
        self.car = Car()

    def quit_choice(self, choice):
        """Check if user wants to quit (entered 'q' or 'Q')"""
        if choice == "q" or choice == "Q":
            print("Returning back to menu....\n")
            time.sleep(0.5)
            return True
        return False

    def main_menu(self):
        """Display main menu and handle choices"""
        print("="*30)
        print("WELCOME TO OUR CAR RENTAL SYSTEM")

        self.main_menu_interface()
        self.choice_main()

    def main_menu_interface(self):

        print("=" * 30)
        print("Please choose from the following options:")
        print("1. Login")
        print("2. Create new account")
        print("3. Login as an Administrator")
        print("4. Exit")
        print("=" * 30)

    def choice_main(self):
        while True:
            choice = input("\nEnter your choice here: ")
            try:

                if choice == "1":
                    time.sleep(0.5)
                    if self.customer.login():
                        time.sleep(0.5)
                        self.user_menu()
                    else:
                        self.main_menu()

                elif choice == "2":
                    time.sleep(0.5)
                    if not self.customer.create_an_account():
                        return self.main_menu()

                elif choice == "3":
                    if self.admin.login():
                        self.admin_menu()
                    else:
                        self.main_menu()

                elif choice == "4":
                    print("Thank you for using OUR CAR RENTAL SYSTEM")
                    exit()

                if not choice.isdigit():
                    raise TypeError

                if not 1 <= int(choice) <= 4:
                    raise ValueError

                self.main_menu_interface()

            except TypeError:
                print("Error: You did not enter a number. Please enter a number from 1 ----> 4")

            except ValueError:
                print("Please enter a number from 1 ----> 4")

    def user_menu(self):
        """Display user menu and handle choices"""
        self.user_menu_interface()
        self.choice_user()

    def user_menu_interface(self):
        print("=" * 30)
        print(f"Mr./ Mrs {self.customer.name.upper()}'s Dashboard")
        print("=" * 30)
        print("1. Rent a Car")
        print("2. Return Car")
        print("3. Check Status")
        print("4. Update Balance")
        print("5. Update Your Information")
        print("6. View All Available Cars")
        print("7. View Specific Car")
        print("8. View Your Rental History")
        print("9. View A Car's Rental History")
        print("10. Have any complain? Feel free to write it in your feedback!")
        print("11. Exit")
        print("=" * 30)
        print("Please choose from the following options:")
        print("Note: Once you exit the user menu, you have to then login again\n")

    def choice_user(self):
        while True:
            try:
                choice = input("\nEnter your choice here: ")

                if choice == "1":
                    if not self.customer.renting():
                        return self.user_menu()
                    self.user_menu()

                elif choice == "2":
                    print("Press q/Q at anytime to quit.")
                    if not self.customer.returning():
                        return self.user_menu()
                    self.user_menu()

                elif choice == "3":
                    self.customer.display_user_info()
                    self.user_menu()

                elif choice == "4":
                    self.customer.update_balance()
                    self.user_menu()

                elif choice == "5":
                    self.customer.update_info()
                    self.user_menu()

                elif choice == "6":
                    self.car.display_all_vehicles()
                    self.user_menu()

                elif choice == "7":
                    self.car.display_vehicle_info()
                    self.user_menu()

                elif choice == "8":
                    self.customer.user_rental_history()
                    self.user_menu()

                elif choice == "9":
                    self.car.cars_rental_history()
                    self.user_menu()

                elif choice == "10":
                    self.customer.write_feedback()
                    self.user_menu()

                elif choice == "11":
                    print("Returning back to main menu....\n")
                    self.main_menu()

                #  EXCEPTION: Invalid entry
                if not choice.isdigit():
                    raise TypeError
                #  EXCEPTION: Invalid number entry
                if int(choice) < 1 or int(choice) > 11:
                    raise ValueError

            #  HANDLING: Invalid entry
            except TypeError:
                print("Error: You did not enter a number. Please enter a number from 1 ----> 11")

            #  HANDLING: Invalid number entry
            except ValueError:
                print("Please enter a number from 1 ----> 11")

    def admin_menu(self):
        """Display user menu and handle choices"""
        self.admin_menu_interface()
        self.choice_admin()

    def admin_menu_interface(self):
        print("=" * 30)
        print(f"ADMIN's Dashboard")
        print("=" * 30)
        print("1. Add Car Fleet")
        print("2. Remove Car Fleet")
        print("3. Remove Specific Car")
        print("4. Check All Customers")
        print("5. Check Specific Customer Rental History")
        print("6. Check Current Rentals")
        print("7. Currently Reserved Cars")
        print("8. View All Available Cars")
        print("9. View All Car IDs")
        print("10. View Specific Car")
        print("11. Access Feedbacks")
        print("12. Update Password")
        print("13. Exit")
        print("=" * 30)
        print("Please choose from the following options:")

    def choice_admin(self):
        while True:
            print("Press q/Q at anytime to quit.")
            try:
                choice = input("\nEnter your choice here: ")

                if choice == "1":
                    self.admin.add_new_car_fleet()
                    self.admin_menu()

                elif choice == "2":
                    self.admin.remove_car_fleet()
                    self.admin_menu()

                elif choice == "3":
                    self.admin.remove_specific_car()
                    self.admin_menu()

                elif choice == "4":
                    self.admin.display_all_users()
                    self.admin_menu()

                elif choice == "5":
                    self.admin.display_user_info()
                    self.admin_menu()

                elif choice == "6":
                    self.admin.check_current_rentals()
                    self.admin_menu()

                elif choice == "7":
                    self.admin.display_reserved_cars()
                    self.admin_menu()

                elif choice == "8":
                    self.car.display_all_vehicles()
                    self.admin_menu()

                elif choice == "9":
                    self.admin.display_car_id()
                    self.admin_menu()

                elif choice == "10":
                    self.car.display_vehicle_info()
                    self.admin_menu()

                elif choice == "11":
                    self.admin.access_feedbacks()

                elif choice == "12":
                    self.admin.update_info()
                    self.admin_menu()

                elif choice == "13":
                    print("Returning back to main menu....\n")
                    self.main_menu()

                #  EXCEPTION: Invalid entry
                if not choice.isdigit():
                    raise TypeError
                #  EXCEPTION: Invalid number entry
                if int(choice) < 1 or int(choice) > 13:
                    raise ValueError

            #  HANDLING: Invalid entry
            except TypeError:
                print("Error: You did not enter a number. Please enter a number from 1 ----> 13")

            #  HANDLING: Invalid number entry
            except ValueError:
                print("Please enter a number from 1 ----> 13")
