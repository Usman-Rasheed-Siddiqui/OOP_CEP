# Import the RentalManager class from the rental_manager module in the current package
from .rental_manager import RentalManager

# Define the list of public objects of this module,
# so when using 'from package import *', only RentalManager will be imported
__all__ = ["RentalManager"]