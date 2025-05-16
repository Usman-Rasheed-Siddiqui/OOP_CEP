
class AlreadyRentedError(Exception):
    pass

class CarNotAvailableError(Exception):
    def __init__(self):
        self.message = "Car with this brand and model is not available. Please try again."
        super().__init__(self.message)

    def __str__(self):
        return self.message

class CarNotRentedError(Exception):
    def __init__(self):
        self.message = "Car with this brand and model does not seem to match our record. Please try again."
        super().__init__(self.message)

    def __str__(self):
        return self.message

class InsufficientBalanceError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

class CustomerNoRentsError(Exception):
    def __init__(self):
        self.message = "You haven't rented any car yet. Please rent a new car using our system"
        super().__init__()

    def __str__(self):
        return self.message

class AccountNotFoundError(Exception):
    def __init__(self):
        self.message = "Account with this name not found"

    def __str__(self):
        return self.message

class WrongPasswordError(Exception):
    def __init__(self):
        self.message = "Password mismatch. No attempts left"
        super().__init__(self.message)

    def __str__(self):
        return self.message

class PasswordError(Exception):
    pass

class ChoiceError(Exception):
    pass