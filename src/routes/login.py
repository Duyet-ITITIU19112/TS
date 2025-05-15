from flask import Blueprint, session, redirect, request, jsonify, url_for, render_template
from src.controllers.login_controller import LoginController
from src.services.onedrive_service import fetch_onedrive_files
from src.utils.msal_helper import initiate_auth_flow
import requests

api = Blueprint("api", __name__)

@api.route("/login")
def login():
    session.pop("flow", None)  # Clear old flow data
    flow = initiate_auth_flow()
    session["flow"] = flow
    return redirect(flow["auth_uri"])


@api.route("/login/authorized")
def authorized():
    try:
        # Retrieve the flow object from the session
        flow = session.pop("flow", None)
        if not flow:
            print("Flow is missing or expired.")
            return jsonify({"error": "Session state missing or expired. Please try logging in again."}), 400

        # Debugging: Log the saved and returned state
        print(f"Saved state: {flow.get('state')}")
        print(f"Returned state: {request.args.get('state')}")

        # Validate the state parameter
        if flow.get("state") != request.args.get("state"):
            print("State mismatch detected!")
            return jsonify({"error": "State mismatch. Please try logging in again."}), 400

        # Authorize the user and create a User model
        user = LoginController.authorize_user(flow, request.args)
        session["user"] = user.to_dict()  # Save user in session
        return redirect(url_for("api.onedrive_ui"))

    except Exception as e:
        print(f"Unexpected error during authorization: {str(e)}")
        return jsonify({"error": str(e)}), 500



@api.route("/onedrive", methods=["GET"])
def onedrive_ui():
    """
    Serve the main OneDrive UI, displaying the root folder.
    """
    return render_template("onedrive.html")  # Load the root page


@api.route("/onedrive/folder/<folder_id>")
def fetch_folder_contents(folder_id):
    print(f"Fetching contents for folder ID: {folder_id}")  # Debugging log
    access_token = session.get("user", {}).get("access_token")
    if not access_token:
        print("Access token is missing or expired.")  # Debugging log
        return jsonify({"error": "User not logged in or session expired."}), 401

    try:
        url = f"https://graph.microsoft.com/v1.0/me/drive/items/{'root' if folder_id == 'root' else folder_id}/children"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        print(f"Graph API response status: {response.status_code}")  # Debugging log
        if response.status_code == 200:
            return jsonify(response.json()["value"])  # Return folder contents
        else:
            error_message = response.json().get("error", {}).get("message", "Unknown error")
            print(f"Error from Graph API: {error_message}")  # Debugging log
            return jsonify({"error": error_message}), response.status_code
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Debugging log
        return jsonify({"error": str(e)}), 500
