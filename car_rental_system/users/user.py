
class User:
    def __init__(self, first_name, last_name, user_id, email, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
        self.email = email
        self.phone_number = phone_number

    def show_profile(self):
        return f'Name: {self.first_name} {self.last_name}\nID: {self.user_id}\nEmail: {self.email}\nPhone number: {self.phone_number}'

