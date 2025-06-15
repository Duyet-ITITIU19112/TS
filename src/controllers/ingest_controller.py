from src.services.microsoft_graph import MicrosoftGraphService
from src.services.parser import parse_file_content
from src.services.elastic_service import index_document
from src.models import db
from src.models.document_model import Document

def ingest_user_onedrive_files(user):
    """
    Pulls OneDrive files for a user, parses and indexes them.
    """
    graph = MicrosoftGraphService(user.access_token)
    files = graph.list_root_files()

    for f in files:
        # Skip if already indexed (optional optimization)
        existing = Document.query.filter_by(filename=f["name"], user_id=user.id).first()
        if existing:
            continue

        file_bytes = graph.fetch_file_content(f["id"])
        text = parse_file_content(f["name"], file_bytes)

        # Index into Elasticsearch
        index_document(user.id, f["name"], text)

        # Save metadata to DB
        doc = Document(
            filename=f["name"],
            source="onedrive",
            user_id=user.id,
            indexed=True
        )
        db.session.add(doc)

    db.session.commit()
