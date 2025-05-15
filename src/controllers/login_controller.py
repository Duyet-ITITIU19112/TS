from src.utils.msal_helper import initiate_auth_flow, acquire_auth_token
from src.services.onedrive_service import fetch_onedrive_files
from src.models.user import User

class LoginController:
    @staticmethod
    def initiate_login():
        # Start the auth flow
        return initiate_auth_flow()

    @staticmethod
    def authorize_user(flow, request_args):
        # Acquire tokens
        token_response = acquire_auth_token(flow, request_args)

        if "access_token" not in token_response:
            raise Exception(f"Token acquisition failed: {token_response.get('error_description')}")

        access_token = token_response["access_token"]
        # Optionally, fetch user info from Microsoft Graph API
        user_info = LoginController.fetch_user_info(access_token)
        return User.from_ms_graph(user_info, access_token)

    @staticmethod
    def fetch_user_info(access_token):
        # Fetch user profile info from Microsoft Graph API
        import requests
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch user info.")
