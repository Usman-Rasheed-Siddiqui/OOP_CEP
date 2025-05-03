from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, first_name="", last_name="", password=""):
        self.first_name = first_name
        self.last_name = last_name
        self.name = self.first_name+" "+last_name
        self.password = password

    @abstractmethod
    def display_user_info(self):
        pass



