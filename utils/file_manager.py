import shutil

class FileManager:
    """
    Utility class for file operations.
    Provides general-purpose functions like creating a working copy.
    """

    @staticmethod
    def create_working_copy(original_file: str, working_copy: str):
        """
        Creates a working copy of a file.

        Args:
            original_file (str): Path to the original file.
            working_copy (str): Path to the working copy.

        Raises:
            Exception: If there is an error during the creation of the copy.
        """
        try:
            shutil.copy(original_file, working_copy)
            print(f"Working copy created at {working_copy}.")
        except Exception as e:
            print(f"Error creating working copy: {e}")
