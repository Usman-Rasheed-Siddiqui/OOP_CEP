# Import the Interface class from the main_interface module
from main_interface import Interface

# Standard Python command to check if this script is being run directly
if __name__ == '__main__':
    # Create an instance of the Interface class
    app = Interface()

    # Call the clear_screen method to clear the display
    app.clear_screen()

    # Call the main_menu method to display the main menu interface
    app.main_menu()