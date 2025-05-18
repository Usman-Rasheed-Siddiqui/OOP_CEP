from abc import ABC, abstractmethod
from exception_handling.Exceptions import PasswordError
from re import search, match
import time

class User(ABC):
    def __init__(self, first_name="", last_name="", password="", email=""):
        self.first_name = first_name
        self.last_name = last_name
        self.name = self.first_name+" "+self.last_name
        self.password = password
        self.email = email
        self.bold_italics = '\033[1m\033[3m'
        self.reset = '\033[0m'

    @abstractmethod
    def display_user_info(self):
        pass

    @staticmethod
    def enter_to_continue():
        while input("Press Enter to continue...") != "":
            print("Please just press Enter without typing anything.")


    def quit_choice(self, choice):
        """Check if user wants to quit (entered 'q' or 'Q')"""
        if choice == "q" or choice == "Q":
            print("Returning back to menu.....\n")
            time.sleep(0.5)
            return True
        return False

    def login(self):
        print("Press q/Q at any time to quit\n")
        while True:
            try:
                self.email = input("Enter your email: ").strip()
                if self.quit_choice(self.email):
                    return False
                if not self.email:
                    raise ValueError("Please enter a valid email")
                break
            except ValueError as e:
                print("Error:", e)


        while True:
            try:
                self.password = input("Enter your password: ").strip()
                if self.quit_choice(self.password):
                        return False
                if not self.password:
                    raise ValueError("Please enter a password")
                break
            except ValueError as e:
                print("Error:", e)

        return True

    def update_info(self, member):
        print("=" * 30)
        print("UPDATE INFORMATION")
        print("=" * 30)
        print()
        print("Press q/Q at any time to quit")
        print("If you don't want to change something, just press enter.")
        print()

        self.password = input("Enter your new password (8+ characters): ").strip()
        if self.quit_choice(self.password):
            return
        if self.password != "":
            self.validate_new_password(self.password)
            member["password"] = self.password
        else:
            self.password = member["password"]
            member["password"] = self.password

    def validate_new_password(self, password):
        if len(password) < 8:
            raise PasswordError("Password should be more than 8 characters")

        error = []
        if not search(r"[0-9]", password):
            error.append("numbers")
        if not search(r"[a-zA-Z]", password):
            error.append("letters")
        if not search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            error.append("special characters")

        if error:
            raise PasswordError(f"Password must contain: {", ".join(error)}")
        return True

    def validate_email(self, email):

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not match(pattern, email):
            raise ValueError("Invalid email format. Example: user@example.com")
        return True