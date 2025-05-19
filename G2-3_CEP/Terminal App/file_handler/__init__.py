# Import the FileHandler class from the file_handler module in the current package
from .file_handler import FileHandler

# Define the list of public objects of this module,
# so when using 'from package import *', only RentalManager will be imported
__all__ = ["FileHandler"]