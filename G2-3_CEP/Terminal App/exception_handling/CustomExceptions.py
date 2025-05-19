class AlreadyRentedError(Exception):
    """Exception raised when a customer tries to rent another car while already having one rented/ When a car is already rented"""
    pass


class CarNotAvailableError(Exception):
    """Exception raised when a requested car is not available for rental."""

    def __init__(self):
        """Initialize the exception with a default message."""
        self.message = "Car with this brand and model is not available. Please try again."
        super().__init__(self.message)

    def __str__(self):
        """Return the exception message when converted to string."""
        return self.message


class CarNotRentedError(Exception):
    """Exception raised when trying to return a car that isn't in the rental records."""

    def __init__(self):
        """Initialize the exception with a default message."""
        self.message = "Car with this ID does not seem to match our rental record. Please try again."
        super().__init__(self.message)

    def __str__(self):
        """Return the exception message when converted to string."""
        return self.message


class InsufficientBalanceError(Exception):
    """Exception raised when a customer doesn't have enough balance to complete a rental."""

    def __init__(self, message):
        """
        Initialize the exception with a custom message.

        Args:
            message (str): Custom error message describing the balance issue
        """
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        """Return the exception message when converted to string."""
        return self.message


class CustomerNoRentsError(Exception):
    """Exception raised when a customer with no rentals tries to perform a return operation."""

    def __init__(self):
        """Initialize the exception with a default message."""
        self.message = "You haven't rented any car yet. Please rent a new car using our system"
        super().__init__()

    def __str__(self):
        """Return the exception message when converted to string."""
        return self.message


class AccountNotFoundError(Exception):
    """Exception raised when a requested account cannot be found in the system."""

    def __init__(self):
        """Initialize the exception with a default message."""
        self.message = "Account with this email not found"
        super().__init__(self.message)

    def __str__(self):
        """Return the exception message when converted to string."""
        return self.message


class WrongPasswordError(Exception):
    """Exception raised when incorrect password is entered multiple times."""

    def __init__(self):
        """Initialize the exception with a default message."""
        self.message = "Password mismatch. No attempts left"
        super().__init__(self.message)

    def __str__(self):
        """Return the exception message when converted to string."""
        return self.message


class PasswordError(Exception):
    """General exception for password-related errors (e.g., weak password, duplicate password)."""
    pass


class ChoiceError(Exception):
    """Exception raised for invalid menu choices or selections."""
    pass


class CarNotFoundError(Exception):
    """Exception raised when a requested car cannot be found in the system."""
    pass