from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, Record

qdrant = QdrantClient(":memory:") #in-memory database

qdrant.recreate_collection(
	collection_name="issues-cosine",
	vectors_config=VectorParams(size=1536, distance=Distance.COSINE))

qdrant.recreate_collection(
	collection_name="issues-euclid",
	vectors_config=VectorParams(size=1536, distance=Distance.EUCLID))

all_data = vectordb.get(include=["embeddings"])
ids = all_data['ids']  # strings
vectors = all_data['embeddings']

records = []
for id, vec in zip(ids, vectors):
  records.append(Record(id=int(id), vector=vec, payload={'issue': id}))

qdrant.upload_records(collection_name="issues-cosine", records=records)
qdrant.upload_records(collection_name="issues-euclid", records=records)
