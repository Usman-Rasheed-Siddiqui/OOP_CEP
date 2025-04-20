import json

class FileHandler():

    @staticmethod
    def save_to_file(data, filename):
        """Saves information to txt file in key = value format"""
        with open(filename, "w") as file:
            for item in data:
                file.write(f"{item.__dict__}\n")

    @staticmethod
    def load_from_file(cls,filename):
        """Loads information from txt file in key = value format"""
        data = []
        try:
            with open(filename, "r") as file:
                for line in file.readlines():
                    attribute_info = json.loads(line.strip())
                    data.append(cls(**attribute_info))
        except FileNotFoundError:
            return []
        return data



