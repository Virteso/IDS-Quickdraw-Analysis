from google.cloud import storage
import os

def download_from_folder(bucket_name, folder_path, destination_folder):
    """
    Download files from a specific folder in a Google Cloud Storage bucket.

    :param bucket_name: Name of the GCS bucket.
    :param folder_path: The "folder" path in the bucket (e.g., "full/simplified/").
    :param destination_folder: Local directory to save the downloaded files.
    """
    # Initialize the anonymous client
    client = storage.Client.create_anonymous_client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=folder_path)

    # Ensure the destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    print(f"Downloading files from folder '{folder_path}' in bucket '{bucket_name}' to '{destination_folder}'")

    # Download files
    for blob in blobs:
        if blob.name.endswith("/"):  # Skip empty folder-like blobs
            continue

        # Define the local file path
        local_file_path = os.path.join(destination_folder, blob.name[len(folder_path):])

        # Create directories for nested paths
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

        # Download the file
        blob.download_to_filename(local_file_path)
        print(f"Downloaded {blob.name} to {local_file_path}")

    print("Download complete.")


# Example usage
bucket_name = "quickdraw_dataset"
data_folders = ["binary/", "numpy_bitmap/", "raw/", "simplified/"]
folder_path = "full/" + data_folders[1]  # The folder you want to download
destination_folder = ".././data/numpy_bitmap"  # Destination folder
download_from_folder(bucket_name, folder_path, destination_folder)