import pandas as pd
import numpy as np
from rank_bm25 import BM25Okapi
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import string
import torch as torch

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('Sahajtomar/sts-GBERT-de')



file_one=pd.read_csv("data.csv")


attribution=[]



query="Logiernächte"

embeddings1 = model.encode(query, convert_to_tensor=True)
embeddings2 = model.encode(file_one.text, convert_to_tensor=True)
cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)
print(cosine_scores)



max_value = torch.max(cosine_scores)
print(max_value)
which=torch.argmax(cosine_scores)
print(which)



attribution.append(str(file_one.title_slug[int(which)])+" ("+str(int(100*max_value))+")")
    

print(attribution)