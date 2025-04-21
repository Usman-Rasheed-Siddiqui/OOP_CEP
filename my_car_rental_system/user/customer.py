from user import User

class Customer(User):
    def __init__(self, first_name, last_name, password, address, balance):
        super().__init__(first_name, last_name, password)
        self.address = address
        self.balance = balance

    def display_user_info(self):
        return f"""
{"="*30}
USER INFORMATION
{"="*30}
Name : {self.name}
Address : {self.address}
Balance : {self.balance}
{"="*30}
"""
    def renting(self):
        pass            # Needs method from rental_manager

    def returning(self):
        pass            # Needs method from rental_manager

    def reservation_receipt(self):      # Needs rental_manager to be completed
        return f"""     
"""
