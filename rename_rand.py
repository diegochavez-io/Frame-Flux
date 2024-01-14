import os
import random
import string

def rename_files_in_folder(folder_path):
    """
    This function renames all the files in the specified folder with a unique random set of numbers and letters.
    The new file names will be 10 characters long and will keep the original file extension.
    """
    for filename in os.listdir(folder_path):
        # Get the file extension
        ext = os.path.splitext(filename)[1]

        # Generate a new random file name of 10 characters
        new_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ext

        # Rename the file
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))

# Use the function to rename all files in your folder
rename_files_in_folder(r"D:\feather_TD\feather_TDMovieOut.0_1" )



