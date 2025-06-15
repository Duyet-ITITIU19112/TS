import requests

class OneDriveServiceError(Exception):
    """Custom exception for OneDrive access issues."""
    pass

class MicrosoftGraphService:
    BASE_URL = "https://graph.microsoft.com/v1.0"

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

    def list_root_files(self) -> list:
        """
        List OneDrive files from the root directory.
        Filters for `.txt` and `.docx` only.
        """
        url = f"{self.BASE_URL}/me/drive/root/children"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            raise OneDriveServiceError(self._extract_error(response))

        data = response.json()
        files = data.get("value", [])

        return [
            file for file in files
            if file.get("file") and file["name"].endswith((".txt", ".docx"))
        ]

    def fetch_file_content(self, file_id: str) -> bytes:
        """
        Stream file content from OneDrive (in memory).
        """
        url = f"{self.BASE_URL}/me/drive/items/{file_id}/content"
        response = requests.get(url, headers=self.headers, stream=True)

        if response.status_code != 200:
            raise OneDriveServiceError(self._extract_error(response))

        return response.content

    def get_user_info(self) -> dict:
        """
        Fetch user profile data (email, name, ID) from Microsoft.
        """
        url = f"{self.BASE_URL}/me"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            raise OneDriveServiceError(self._extract_error(response))

        return response.json()

    def _extract_error(self, response) -> str:
        try:
            return response.json().get("error", {}).get("message", "Unknown error")
        except Exception:
            return f"HTTP {response.status_code}"
