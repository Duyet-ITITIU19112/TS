import os
import msal

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = "https://login.microsoftonline.com/common"
REDIRECT_URI = "http://localhost:5000/api/login/authorized"
SCOPES = ["Files.Read", "User.Read"]

# Create MSAL instance
msal_app = msal.ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)

# Initiate the authorization flow
def initiate_auth_flow():
    return msal_app.initiate_auth_code_flow(SCOPES, redirect_uri=REDIRECT_URI)

# Acquire an access token after login
def acquire_auth_token(flow, request_args):
    return msal_app.acquire_token_by_auth_code_flow(flow, request_args)
