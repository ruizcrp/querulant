import pandas as pd
import numpy as np
import string
import torch as torch
import time

from sentence_transformers import SentenceTransformer, util



class QueryControler(object):
    def __init__(self,file_one):
    self.model = SentenceTransformer('Sahajtomar/sts-GBERT-de')
    self.file_one=file_one
    self.embeddings2 =  model.encode(self.file_one.text, convert_to_tensor=True)

    def lookup_query(self,query):
        start = time.time()
        embeddings1 = model.encode(query, convert_to_tensor=True)
        cosine_scores = util.pytorch_cos_sim(embeddings1, self.embeddings2)

        max_value = torch.max(cosine_scores)
        which=torch.argmax(cosine_scores)
        end = time.time()
        time_elapsed=str(round(end-start,1))
        return(str(self.file_one.title[int(which)])+" ("+str(int(100*max_value))+" perc) gefunden in "+time_elapsed+" Sekunden.")


   
