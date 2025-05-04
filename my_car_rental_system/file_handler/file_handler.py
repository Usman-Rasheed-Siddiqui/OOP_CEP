import os

class FileHandler:

    def save_to_file(self, data, file):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = os.path.join(base_dir, "data", file)
        with open(file, 'w') as f:
            for item in data:
                f.write(str(item)+"\n")

    def load_from_file(self, file):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = os.path.join(base_dir, "data", file)
        data = []

        try:
            with open(file, 'r') as f:
                for line in f:
                    data.append(eval(line))

        except FileNotFoundError:
            pass
        return data

    def create_file(self, directory, name):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sec_dir = os.path.join(base_dir, "data", directory)

        safe_name = name.replace(" ", "_")
        file = os.path.join(sec_dir, f"{safe_name}.txt")

        with open(file, 'w') as f:
            pass