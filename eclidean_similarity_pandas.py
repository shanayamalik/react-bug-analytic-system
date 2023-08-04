#importing packages
import numpy as np
import pandas as pd
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer
import json
from time import sleep

print("working...")
sleep(.5)
print("Extracting data from Json File...")
sleep(.5)
print("Embedding file this will take a minute...")
sleep(.5)
print("Please hold while I work...")
# Define the model we want to use (it'll download itself)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
