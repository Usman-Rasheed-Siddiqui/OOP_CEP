import os


class FileHandler:
    """
    A class to handle file operations including saving, loading, and creating files.
    Manages all file interactions for the application with proper path handling.
    """

    def save_to_file(self, data, file):
        """
        Save data to a specified file in the application's data directory.
        """

        # Construct absolute path to the data directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = os.path.join(base_dir, "data", file)

        # Write each item in data as a new line in the file
        with open(file, 'w') as f:
            for item in data:
                f.write(str(item) + "\n")

    def load_from_file(self, file):
        """
        Load data from a specified file in the application's data directory.
        """

        # Construct absolute path to the data directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = os.path.join(base_dir, "data", file)
        data = []

        try:
            # Read each line and evaluate it back to Python object
            with open(file, 'r') as f:
                for line in f:
                    data.append(eval(line.strip()))

        except FileNotFoundError:
            # Silently handle missing files by returning empty list
            pass
        return data

    def create_file(self, directory, email):
        """
        Create a new empty file for a user in a specified subdirectory.

        The filename is derived from the email by replacing special characters.
        """
        # Construct absolute path to the target directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sec_dir = os.path.join(base_dir, "data", directory)

        # Make email safe for filename by replacing special characters
        safe_email = email.replace("@", "_at_").replace(".", "_dot_")
        file = os.path.join(sec_dir, f"{safe_email}.txt")

        # Create parent directories if they don't exist
        os.makedirs(sec_dir, exist_ok=True)

        # Create empty file
        with open(file, 'w') as f:
            pass