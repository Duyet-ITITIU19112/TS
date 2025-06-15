import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch import exceptions as es_exceptions  # Updated import

# Load environment variables
load_dotenv()

ES_HOST     = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
ES_USERNAME = os.getenv("ELASTICSEARCH_USERNAME", "elastic")
ES_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD", "111111")
VERIFY_CERTS = False
INDEX_NAME   = os.getenv("ELASTICSEARCH_INDEX", "test-index")

es = Elasticsearch(
    hosts=[ES_HOST],
    basic_auth=(ES_USERNAME, ES_PASSWORD),
    verify_certs=VERIFY_CERTS,
    retry_on_timeout=True,
    request_timeout=60,
    max_retries=3
)

def ensure_index():
    try:
        if not es.indices.exists(index=INDEX_NAME):
            es.indices.create(
                index=INDEX_NAME,
                settings={"number_of_shards": 1, "number_of_replicas": 0},
                mappings={
                    "properties": {
                        "filename": {"type": "keyword"},
                        "content": {"type": "text"}
                    }
                }
            )
    except es_exceptions.ElasticsearchException as e:
        print("❌ Failed to create index:", e)
        raise

def index_document(doc_id, filename, content):
    ensure_index()
    try:
        res = es.index(index=INDEX_NAME, id=doc_id, document={
            "filename": filename,
            "content": content
        })
        print(f"✅ Document {doc_id} indexed: {res['result']}")
    except es_exceptions.ElasticsearchException as e:
        print(f"❌ Failed to index document {doc_id}:", e)
        raise

def search_bm25(query, top_k=5):
    ensure_index()
    body = {"query": {"match": {"content": {"query": query}}}}
    try:
        res = es.search(index=INDEX_NAME, body=body, size=top_k)
        hits = res["hits"]["hits"]
        print(f"🔍 Top {len(hits)} results for '{query}':")
        for hit in hits:
            score = hit["_score"]
            src = hit["_source"]
            print(f" - [{score:.2f}] {src.get('filename')}: {src.get('content')}")
        return hits
    except es_exceptions.ElasticsearchException as e:
        print("❌ Search failed:", e)
        raise
