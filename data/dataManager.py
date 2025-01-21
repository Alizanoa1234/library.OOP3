import pandas as pd

class DataManager:
    """
    Singleton class to manage the shared DataFrame for the library system.
    """
    _instance = None  # Instance for Singleton
    _data_frame = None  # Shared DataFrame

    @staticmethod
    def get_instance():
        if DataManager._instance is None:
            DataManager()
        return DataManager._instance

    def __init__(self):
        if DataManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DataManager._instance = self

    def initialize_data(self, data_frame: pd.DataFrame):
        """
        Initialize the shared DataFrame.

        Args:
            data_frame (pd.DataFrame): The initial DataFrame to manage.
        """
        DataManager._data_frame = data_frame

    @staticmethod
    def get_data():
        """
        Get the shared DataFrame.

        Returns:
            pd.DataFrame: The managed DataFrame.
        """
        return DataManager._data_frame

    @staticmethod
    def save_to_file(file_path: str):
        """
        Save the DataFrame to a CSV file.

        Args:
            file_path (str): The file path where the DataFrame should be saved.
        """
        DataManager._data_frame.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}.")
