
class FileHandler:

    def save_to_file(self, data, file):
        with open(file, 'w') as file:
            for item in data:
                file.write(str(item)+"\n")

    def load_from_file(self, file):
        data = []
        with open(file, 'r') as file:
            for line in file:
                data.append(eval(line))

        return data