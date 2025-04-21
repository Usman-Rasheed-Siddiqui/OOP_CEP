from user import User

class Admin(User):
    def __init__(self, first_name, last_name, password):
        super().__init__(first_name, last_name, password)

    def display_user_info(self):
        pass

    def manage_rental(self):    # Needs Rental Manager to complete
        pass

    def manage_return(self):    # Needs Rental Manager to complete
        pass

    def add_a_new_car(self):
        pass                    # Needs Rental Manager to complete

    def  remove_car(self):
        pass                    # Needs Rental Manager to complete

    def print_customers_report(self):   # Needs Rental Manager to complete
        customer_report = []
        return f"""
"""

    def access_feedbacks(self):
        pass                        # Needs File Handler File to be completed