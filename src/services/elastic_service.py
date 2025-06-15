from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv
load_dotenv()

es = Elasticsearch(
    os.getenv("ELASTICSEARCH_URL", "http://localhost:9200"),
    basic_auth=(
        os.getenv("ELASTICSEARCH_USERNAME"),
        os.getenv("ELASTICSEARCH_PASSWORD")
    ),
    # verify_certs=(os.getenv("ELASTICSEARCH_VERIFY_CERTS", "false") == "true"),
    # ca_certs=os.getenv("ELASTICSEARCH_CA_CERT_PATH") or None
)

INDEX_NAME = "user_files"

def index_document(user_id: int, filename: str, content: str):
    doc = {
        "user_id": user_id,
        "filename": filename,
        "content": content,
    }

    es.index(index=INDEX_NAME, body=doc)
def search_bm25(query: str, user_id: int, top_k: int = 500):
    response = es.search(index=INDEX_NAME, body={
        "size": top_k,
        "query": {
            "bool": {
                "must": [
                    {"match": {"content": query}},
                    {"term": {"user_id": user_id}}
                ]
            }
        }
    })

    hits = response.get("hits", {}).get("hits", [])
    return [
        {
            "id": hit["_id"],
            "score": hit["_score"],
            "filename": hit["_source"]["filename"],
            "content": hit["_source"]["content"]
        }
        for hit in hits
    ]
def create_index_if_not_exists():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body={
            "mappings": {
                "properties": {
                    "user_id": {"type": "integer"},
                    "filename": {"type": "text"},
                    "content": {
                        "type": "text",
                        "analyzer": "standard"
                    }
                }
            }
        })
