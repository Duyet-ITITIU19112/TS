import requests


class OneDriveServiceError(Exception):
    """Custom exception class for OneDrive service errors."""
    pass


def fetch_onedrive_files(access_token):
    """
    Fetches files and folders from the user's OneDrive root directory.

    Args:
        access_token (str): The OAuth access token used for API requests.

    Returns:
        list: A list of files and folders in the OneDrive root directory.

    Raises:
        OneDriveServiceError: If the request fails or the API returns an error.
    """
    # Define the Microsoft Graph API endpoint
    url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Parse and return file/folder data
        return response.json()["value"]
    else:
        # Handle API errors
        error_message = response.json().get("error", {}).get("message", "Unknown error")
        raise Exception(f"Failed to fetch OneDrive files: {error_message}")
