
class FileHandler:

    def save_to_file(self, data, file):
        with open(file, 'w') as file:
            file.write(data)

    def load_from_file(self, file):
        with open(file, 'r') as file:
            data = file.read().strip()

        return data