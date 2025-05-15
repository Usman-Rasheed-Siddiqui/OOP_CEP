from abc import ABC, abstractmethod
from exception_handling.Exceptions import PasswordError
from re import search
import time

class User(ABC):
    def __init__(self, first_name="", last_name="", password=""):
        self.first_name = first_name
        self.last_name = last_name
        self.name = self.first_name+" "+self.last_name
        self.password = password

    @abstractmethod
    def display_user_info(self):
        pass

    def quit_choice(self, choice):
        """Check if user wants to quit (entered 'q' or 'Q')"""
        if choice == "q" or choice == "Q":
            print("Returning back to menu.....\n")
            time.sleep(0.5)
            return True
        return False

    def login(self):
        print("Press q/Q at any time to quit\n")
        self.name = input("Enter your name: ").strip()
        if self.quit_choice(self.name):
            return False

        self.password = input("Enter your password: ").strip()
        if self.quit_choice(self.password):
            return False

        return True

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
