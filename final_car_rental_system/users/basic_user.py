from abc import ABC, abstractmethod
from exception_handling.Exceptions import PasswordError
from re import search

class User(ABC):
    def __init__(self, first_name="", last_name="", password=""):
        self.first_name = first_name
        self.last_name = last_name
        self.name = self.first_name+" "+self.last_name
        self.password = password

    @abstractmethod
    def display_user_info(self):
        pass

    def login(self):
        self.name = input("Enter your name: ").strip()
        self.password = input("Enter your password: ").strip()

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
