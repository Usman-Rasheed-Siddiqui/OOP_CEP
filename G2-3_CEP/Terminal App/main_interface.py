from users.customer import Customer
from vehicle.car import Car
from users.admin import Admin
import time
import os

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

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def main_menu(self):
        """Display main menu and handle choices"""
        print("=" * 45)
        print("      WELCOME TO OUR CAR RENTAL SYSTEM")

        self.main_menu_interface()
        self.choice_main()

    def main_menu_interface(self):

        print("=" * 45)
        print()
        print("Please choose from the following options:")
        print("1. Login as Customer")
        print("2. Create New Account")
        print("3. Login as an Administrator")
        print("4. Exit")
        print()
        print("=" * 45)

    def choice_main(self):
        while True:
            choice = input("\nEnter your choice here: ")
            try:

                if choice == "1":
                    time.sleep(0.5)
                    self.clear_screen()
                    if self.customer.login():
                        time.sleep(0.5)
                        self.clear_screen()
                        self.user_menu()
                    else:
                        self.clear_screen()
                        self.main_menu()

                elif choice == "2":
                    time.sleep(0.5)
                    self.clear_screen()
                    self.clear_screen()
                    if not self.customer.create_an_account():
                        self.clear_screen()
                        self.main_menu()

                    self.main_menu()

                elif choice == "3":
                    self.clear_screen()
                    if self.admin.login():
                        self.clear_screen()
                        self.admin_menu()
                    else:
                        self.clear_screen()
                        self.main_menu()

                elif choice == "4":
                    print("Thank you for using OUR CAR RENTAL SYSTEM")
                    exit()

                if not choice.isdigit():
                    raise TypeError

                if not 1 <= int(choice) <= 4:
                    raise ValueError

                self.clear_screen()
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
        print("=" * 65)
        print(f"    Mr./ Mrs. {self.customer.name.upper()}'s Dashboard")
        print("=" * 65)
        print()
        print("1. Rent a Car")
        print("2. Return Car")
        print("3. Check Status")
        print("4. Update Balance")
        print("5. Update Your Information")
        print("6. View All Available Cars")
        print("7. View Specific Available Car")
        print("8. View Your Rental History")
        print("9. View A Car's Rental History")
        print("10. Have any complain? Feel free to write it in your feedback!")
        print("11. Exit\n")
        print("=" * 65)
        print("\nPlease choose from the following options:")
        print("Note: Once you exit the user menu, you have to then login again")

    def choice_user(self):
        while True:
            try:
                choice = input("\nEnter your choice here: ")

                if choice == "1":
                    self.clear_screen()
                    if not self.customer.renting():
                        self.clear_screen()
                        return self.user_menu()
                    self.clear_screen()
                    self.user_menu()

                elif choice == "2":
                    self.clear_screen()
                    if not self.customer.returning():
                        self.clear_screen()
                        return self.user_menu()
                    self.clear_screen()
                    self.user_menu()

                elif choice == "3":
                    self.clear_screen()
                    self.customer.display_user_info()
                    self.clear_screen()
                    self.user_menu()

                elif choice == "4":
                    self.clear_screen()
                    self.customer.update_balance()
                    self.clear_screen()
                    self.user_menu()

                elif choice == "5":
                    self.clear_screen()
                    self.customer.update_info()
                    self.clear_screen()
                    self.user_menu()

                elif choice == "6":
                    self.clear_screen()
                    self.car.display_all_vehicles()
                    self.clear_screen()
                    self.user_menu()

                elif choice == "7":
                    self.clear_screen()
                    self.car.display_vehicle_info()
                    self.clear_screen()
                    self.user_menu()

                elif choice == "8":
                    self.clear_screen()
                    self.customer.user_rental_history()
                    self.clear_screen()
                    self.user_menu()

                elif choice == "9":
                    self.clear_screen()
                    self.car.cars_rental_history()
                    self.clear_screen()
                    self.user_menu()

                elif choice == "10":
                    self.clear_screen()
                    self.customer.write_feedback()
                    self.clear_screen()
                    self.user_menu()

                elif choice == "11":
                    print("Returning back to main menu....\n")
                    self.clear_screen()
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
        print("=" * 40)
        print(f"           ADMIN's Dashboard")
        print("=" * 40)
        print()
        print("1. Add Car Fleet")
        print("2. Remove Car Fleet")
        print("3. Remove Specific Car")
        print("4. Check All Customers")
        print("5. Check Specific Customer Rental History")
        print("6. Check a Car's Rental History")
        print("7. Check Current Rentals")
        print("8. Currently Reserved Cars")
        print("9. View All Available Cars")
        print("10. View All Available Car IDs")
        print("11. View Specific Car")
        print("12. Access Feedbacks")
        print("13. Update Password")
        print("14. Exit\n")
        print("=" * 40)
        print()
        print("Please choose from the following options:")

    def choice_admin(self):
        while True:
            try:
                choice = input("\nEnter your choice here: ")

                if choice == "1":
                    self.clear_screen()
                    self.admin.add_new_car_fleet()
                    self.clear_screen()
                    self.admin_menu()

                elif choice == "2":
                    self.clear_screen()
                    self.admin.remove_car_fleet()
                    self.clear_screen()
                    self.admin_menu()

                elif choice == "3":
                    self.clear_screen()
                    self.admin.remove_specific_car()
                    self.clear_screen()
                    self.admin_menu()

                elif choice == "4":
                    self.clear_screen()
                    self.admin.display_all_users()
                    self.clear_screen()
                    self.admin_menu()

                elif choice == "5":
                    self.clear_screen()
                    self.admin.display_user_info()
                    self.clear_screen()
                    self.admin_menu()


                elif choice == "6":
                    self.clear_screen()
                    self.car.cars_rental_history()
                    self.clear_screen()
                    self.admin_menu()


                elif choice == "7":
                    self.clear_screen()
                    self.admin.check_current_rentals()
                    self.clear_screen()
                    self.admin_menu()

                elif choice == "8":
                    self.clear_screen()
                    self.admin.display_reserved_cars()
                    self.clear_screen()
                    self.admin_menu()

                elif choice == "9":
                    self.clear_screen()
                    self.car.display_all_vehicles()
                    self.clear_screen()
                    self.admin_menu()

                elif choice == "10":
                    self.clear_screen()
                    self.admin.display_car_id()
                    self.clear_screen()
                    self.admin_menu()

                elif choice == "11":
                    self.clear_screen()
                    self.car.display_vehicle_info()
                    self.clear_screen()
                    self.admin_menu()

                elif choice == "12":
                    self.clear_screen()
                    self.admin.access_feedbacks()
                    self.clear_screen()
                    self.admin_menu()

                elif choice == "13":
                    self.clear_screen()
                    self.admin.update_info()
                    self.clear_screen()
                    self.admin_menu()

                elif choice == "14":
                    print("Returning back to main menu....\n")
                    self.clear_screen()
                    self.main_menu()

                #  EXCEPTION: Invalid entry
                if not choice.isdigit():
                    raise TypeError
                #  EXCEPTION: Invalid number entry
                if int(choice) < 1 or int(choice) > 14:
                    raise ValueError

            #  HANDLING: Invalid entry
            except TypeError:
                print("Error: You did not enter a number. Please enter a number from 1 ----> 14")

            #  HANDLING: Invalid number entry
            except ValueError:
                print("Please enter a number from 1 ----> 14")
