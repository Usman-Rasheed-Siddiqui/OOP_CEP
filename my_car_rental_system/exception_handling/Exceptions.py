
class AlreadyRentedError(Exception):
    pass

class CarNotAvailableError(Exception):
    def __init__(self):
        self.message = "Car with this brand and model is not available"
        super().__init__(self.message)

    def __str__(self):
        return self.message