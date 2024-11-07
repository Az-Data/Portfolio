import requests
import os

# Base GitHub API and raw file URLs
base_api_url = "https://api.github.com/repos/Az-Data/Portfolio/contents/Data"
base_raw_url = "https://github.com/Az-Data/Portfolio/raw/master/Data"

# Define the folder name
folder_name = "Data"

# Check if the folder exists; if not, create it
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print(f"Folder '{folder_name}' created.")
else:
    print(f"Folder '{folder_name}' already exists.")

# Get the absolute path to the 'Contents' folder
destination_path = os.path.abspath(folder_name)


# Function to recursively download files and folders
def download_files_and_folders(api_url, local_path):
    # Ensure the local directory exists
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    
    # Get the list of files/folders in the current directory
    response = requests.get(api_url)
    response.raise_for_status()  # Ensure the request was successful
    items = response.json()
    
    all_exist = True  # Flag to check if all files already exist

    for item in items:
        # Check if it's a file
        if item['type'] == 'file':
            file_url = f"{base_raw_url}/{item['path'][5:]}"  # Adjust path for raw URL
            file_path = os.path.join(local_path, item['name'])

            # Check if file already exists
            if not os.path.exists(file_path):
                # Download the file
                print(f"Downloading {file_path}...")
                file_response = requests.get(file_url, stream=True)
                file_response.raise_for_status()
                with open(file_path, 'wb') as f:
                    for chunk in file_response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                print(f"Downloaded {file_path}")
                all_exist = False
            else:
                print(f"{file_path} already exists.")
        
        # Check if it's a directory and recurse
        elif item['type'] == 'dir':
            subdir_path = os.path.join(local_path, item['name'])
            download_files_and_folders(item['url'], subdir_path)
            all_exist = False

    return all_exist

# Start download from the main 'Data' folder
all_files_exist = download_files_and_folders(base_api_url, destination_path)

if all_files_exist:
    print("All files and folders already exist.")
else:
    print("Download completed.")
