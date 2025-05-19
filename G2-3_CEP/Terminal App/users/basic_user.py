# Import required modules and classes
from abc import ABC, abstractmethod  # For creating abstract base classes
from exception_handling.CustomExceptions import PasswordError  # Custom password exception
from re import search, match  # For regular expression operations
import time  # For adding delays in the interface


class User(ABC):
    """
    Abstract base class representing a user in the system.
    Serves as the foundation for all user types (Customer, Admin, etc.).

    Attributes:
        first_name (str): User's first name
        last_name (str): User's last name
        name (str): Combined first and last name
        password (str): User's password
        email (str): User's email address
        bold_italics (str): ANSI escape codes for bold/italic text
        reset (str): ANSI escape code to reset text formatting
    """

    def __init__(self, first_name="", last_name="", password="", email=""):
        """
        Initialize a User instance with basic properties.

        Args:
            first_name (str): User's first name
            last_name (str): User's last name
            password (str): User's password
            email (str): User's email address
        """
        self.first_name = first_name
        self.last_name = last_name
        self.name = self.first_name + " " + self.last_name  # Combined full name
        self.password = password
        self.email = email
        # ANSI escape codes for text formatting
        self.bold_italics = '\033[1m\033[3m'  # Bold and italic
        self.reset = '\033[0m'  # Reset formatting

    @abstractmethod
    def display_user_info(self):
        """
        Abstract method that must be implemented by child classes.
        Should display information about the user.
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
        """
        if choice == "q" or choice == "Q":
            print("Returning back to menu.....\n")
            time.sleep(0.5)  # Small delay for better UX
            return True
        return False

    def login(self):
        """
        Handle user login process by collecting email and password.
        """
        print("Press q/Q at any time to quit\n")

        # Email input loop with validation
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

        # Password input loop with validation
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

        return True  # Login successful

    def update_info(self, member):
        """
        Update user information (currently only password).
        """
        print("=" * 30)
        print("      UPDATE INFORMATION")
        print("=" * 30)
        print("\nPress q/Q at any time to quit")
        print("If you don't want to change something, just press enter.")
        print("\nNote: Name and Email cannot be Modified")
        print()

        # Get new password input
        self.password = input("Enter your new password (8+ characters): ").strip()
        if self.quit_choice(self.password):
            return

        # Validate and update password if provided
        if self.password != "":
            self.validate_new_password(self.password)
            member["password"] = self.password
        else:
            # Keep existing password if none entered
            self.password = member["password"]
            member["password"] = self.password

    def validate_new_password(self, password):
        """
        Validate that a password meets security requirements.
        """
        # Minimum length check
        if len(password) < 8:
            raise PasswordError("Password should be more than 8 characters")

        error = []
        # Check for numbers
        if not search(r"[0-9]", password):
            error.append("numbers")
        # Check for letters
        if not search(r"[a-zA-Z]", password):
            error.append("letters")
        # Check for special characters
        if not search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            error.append("special characters")

        # Raise error if any requirements not met
        if error:
            raise PasswordError(f"Password must contain: {', '.join(error)}")
        return True

    def validate_email(self, email):
        """
        Validate that an email address is properly formatted.
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not match(pattern, email):
            raise ValueError("Invalid email format. Example: user@example.com")
        return True