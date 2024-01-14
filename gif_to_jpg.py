import os

def rename_files_in_directory(directory, old_ext, new_ext):
    for filename in os.listdir(directory):
        if filename.endswith(old_ext):
            base = os.path.splitext(filename)[0]
            os.rename(
                os.path.join(directory, filename), 
                os.path.join(directory, base + new_ext)
            )

def main():
    directory = "G:\\My Drive\\dataset-footage\\shamoncassette\\tumblr"  # Replace with your directory
    old_ext = ".gifv"
    new_ext = ".jpg"
    rename_files_in_directory(directory, old_ext, new_ext)

if __name__ == "__main__":
    main()
