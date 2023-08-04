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

testissue = 24553

testvec = vectordb.get(ids=[str(testissue)],include=["embeddings"])['embeddings'][0]

l2test = vectordb.query(query_embeddings=[testvec], n_results=20)['ids'][0]

cosinetest = [p.payload['issue'] for p in
              qdrant.search(query_vector=testvec, limit=20,
                            collection_name="issues-cosine")]

euclidtest = [p.payload['issue'] for p in
              qdrant.search(query_vector=testvec, limit=20,
                            collection_name="issues-euclid")]

for l2, cs, ed in zip(l2test, cosinetest, euclidtest):
  print(l2, cs, ed, l2 == cs and cs == ed)

from random import sample

testids = sample(ids, 1000)  # test 1000 out of 7569 at random

allsame = 0
triples = []
for id in testids:
  testvec = vectordb.get(ids=[str(id)],include=["embeddings"])['embeddings'][0]
  l2test = vectordb.query(query_embeddings=[testvec], n_results=20)['ids'][0]
  cosinetest = [p.payload['issue'] for p in qdrant.search(query_vector=testvec,
                                         limit=20, collection_name="issues-cosine")]
  euclidtest = [p.payload['issue'] for p in qdrant.search(query_vector=testvec,
                                         limit=20, collection_name="issues-euclid")]
  if l2test == cosinetest == euclidtest:
    allsame += 1
  triples.append((l2test, cosinetest, euclidtest))

print(allsame)  ### RESULT: 53% of the time all three top-20 are exactly the same (got 526 and 536 from 2 runs)

def weighted_similarity(list1, list2):
    # Total weight is the sum of the weights from 1 to n
    total_weight = sum(range(1, len(list1) + 1))

    # Similarity is the sum of the weights where the elements of the two lists match
    similarity = sum(weight for weight, (el1, el2) in enumerate(zip(list1, list2), 1) if el1 == el2)

    return similarity / total_weight

def common_elements_similarity(list1, list2):
    # Create sets from the lists
    set1 = set(list1)
    set2 = set(list2)

    # Calculate the number of common elements
    common_elements = set1 & set2  # & operator returns the intersection of two sets

    # The similarity is the number of common elements divided by the total possible elements
    similarity = len(common_elements) / max(len(set1), len(set2))

    return similarity

def pairwise_similarity(tuples):  # [(l2, cosine, eudlidean)...] from triples above
    weight_l2cs = common_l2cs = weight_l2ed = common_l2ed = weight_csed = common_csed = 0.0

    for l2, cs, ed in tuples:
        weight_l2cs += weighted_similarity(l2, cs)
        common_l2cs += common_elements_similarity(l2, cs)
        weight_l2ed += weighted_similarity(l2, ed)
        common_l2ed += common_elements_similarity(l2, ed)
        weight_csed += weighted_similarity(cs, ed)
        common_csed += common_elements_similarity(cs, ed)

    return {'weight_l2cs': round(weight_l2cs / len(tuples), 4),
            'common_l2cs': round(common_l2cs / len(tuples), 4),
            'weight_l2ed': round(weight_l2ed / len(tuples), 4),
            'common_l2ed': round(common_l2ed / len(tuples), 4),
            'weight_csed': round(weight_csed / len(tuples), 4),
            'common_csed': round(common_csed / len(tuples), 4)}

pairwise_similarity(triples)

def biggest_difference(tuples):
  smallest = 1000.0
  n = 0

  for l2, cs, ed in tuples:
    sim = weighted_similarity(l2, ed)
    if sim < smallest:
      smallest = sim
      pos = n
      foundl2 = l2
      founded = ed
    n += 1
  id = testids[pos]
  print('L2 and Euclidean for', id, 'similarity', smallest, 'common',
        common_elements_similarity(foundl2, founded))
  for a, b in zip(foundl2, founded):
    print (a, b, '' if a == b else '*')

biggest_difference(triples)
