import os
import msal

# MSAL Configuration
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = "https://login.microsoftonline.com/common"
REDIRECT_URI = "http://localhost:5000/api/login/authorized"
SCOPES = ["Files.Read", "User.Read"]

# Initialize MSAL Confidential Client
msal_app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=AUTHORITY
)

def initiate_auth_flow():
    """
    Initiates the OAuth 2.0 Authorization Code Flow.
    Returns the flow object with the auth URI to redirect the user.
    """
    return msal_app.initiate_auth_code_flow(SCOPES, redirect_uri=REDIRECT_URI)

def acquire_auth_token(flow, request_args):
    """
    Acquires tokens using the authorization code flow.

    Args:
        flow (dict): The flow object stored in session.
        request_args (dict): The arguments from the redirect URL (e.g., state, code).

    Returns:
        dict: The MSAL token response containing access_token, refresh_token, etc.
    """
    return msal_app.acquire_token_by_auth_code_flow(flow, request_args)
