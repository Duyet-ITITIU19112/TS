# from flask import Blueprint, request, jsonify
# import requests
#
# # Define the Blueprint
# search_bp = Blueprint('search', __name__)
#
# # Function to interact with Microsoft Graph API
# def search_files(keyword, access_token):
#     """
#     Search for files in OneDrive using the Microsoft Graph API.
#
#     :param keyword: The keyword to search for.
#     :param access_token: The OAuth2 access token for Microsoft Graph API.
#     :return: List of matching files (name, id, and URL).
#     """
#     url = f"https://graph.microsoft.com/v1.0/me/drive/root/search(q='{keyword}')"
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }
#
#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         raise Exception(f"Error searching for files: {response.status_code} - {response.json()}")
#
#     # Filter only `.doc` and `.docx` files
#     files = [
#         {
#             "name": file["name"],
#             "id": file["id"],
#             "webUrl": file["webUrl"]
#         }
#         for file in response.json().get("value", [])
#         if file["name"].lower().endswith((".doc", ".docx"))
#     ]
#
#     return files
#
# # Define the route for searching files
# @search_bp.route("/search", methods=["GET"])
# def api_search():
#     keyword = request.args.get("keyword", "").strip()
#     access_token = "YOUR_ACCESS_TOKEN"  # Replace with the actual token retrieval logic
#
#     if not keyword:
#         return jsonify({"error": "Keyword is required"}), 400
#
#     try:
#         files = search_files(keyword, access_token)
#         return jsonify({"files": files}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

from flask import Blueprint, request, jsonify, session
from src.services.elastic_service import search_bm25

search_bp = Blueprint("search", __name__, url_prefix="/search")

@search_bp.route("", methods=["GET"])
def search():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401

    q = request.args.get("q", "")
    if not q:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    results = search_bm25(q, user_id, top_k=200)

    # Return filenames and scores (omit full content for perf)
    return jsonify([
        {"id": r["id"], "filename": r["filename"], "score": r["score"]}
        for r in results
    ])
