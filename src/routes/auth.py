import os
from flask import Blueprint, redirect, request, url_for, session, current_app
import requests
from datetime import datetime, timedelta
from src.models.user_model import User
from src.models import db
from src.services.microsoft_graph import MicrosoftGraphService

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login")
def login():
    # Fetch OAuth settings safely with fallback to environment
    client_id = current_app.config.get("CLIENT_ID") or os.getenv("CLIENT_ID")
    tenant    = current_app.config.get("MS_TENANT_ID") or os.getenv("MS_TENANT_ID")
    redirect_uri = current_app.config.get("MS_REDIRECT_URI") or os.getenv("MS_REDIRECT_URI")
    scope     = "User.Read Files.Read offline_access"

    # 🎯 Debug info (optional; remove later)
    print("🔑 CONFIG KEYS:", list(current_app.config.keys()))
    print("🎯 Using MS_REDIRECT_URI:", redirect_uri)

    auth_url = (
        f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize"
        f"?client_id={client_id}"
        f"&response_type=code"
        f"&redirect_uri={redirect_uri}"
        f"&response_mode=query"
        f"&scope={scope}"
    )
    return redirect(auth_url)

@auth_bp.route("/callback")
def callback():
    # Safe retrieval with fallback
    client_id = current_app.config.get("CLIENT_ID") or os.getenv("CLIENT_ID")
    client_secret = current_app.config.get("CLIENT_SECRET") or os.getenv("CLIENT_SECRET")
    tenant = current_app.config.get("MS_TENANT_ID") or os.getenv("MS_TENANT_ID")
    redirect_uri = current_app.config.get("MS_REDIRECT_URI") or os.getenv("MS_REDIRECT_URI")

    token_url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": request.args.get("code"),
        "redirect_uri": redirect_uri,
        "scope": "User.Read Files.Read offline_access"
    }

    token_resp = requests.post(token_url, data=data)
    token_json = token_resp.json()
    access_token = token_json.get("access_token")
    refresh_token = token_json.get("refresh_token")
    expires_in = token_json.get("expires_in")

    if not access_token:
        return f"Token request failed: {token_json}", 400

    expires_at = datetime.utcnow() + timedelta(seconds=int(expires_in))

    ms = MicrosoftGraphService(access_token)
    profile = ms.get_user_info()
    ms_id = profile.get("id")
    email = profile.get("userPrincipalName")
    name = profile.get("displayName")

    user = User.query.filter_by(ms_id=ms_id).first()
    if not user:
        user = User(
            ms_id=ms_id,
            name=name,
            email=email,
            access_token=access_token,
            refresh_token=refresh_token,
            token_expires=expires_at
        )
        db.session.add(user)
    else:
        user.access_token = access_token
        user.refresh_token = refresh_token
        user.token_expires = expires_at

    db.session.commit()
    session["user_id"] = user.id

    from src.controllers.ingest_controller import ingest_user_onedrive_files
    ingest_user_onedrive_files(user)

    return redirect(url_for("files.upload"))
