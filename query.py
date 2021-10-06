import pandas as pd
import numpy as np
import string
import torch as torch
import time

from sentence_transformers import SentenceTransformer, util

import logging
from logging.handlers import RotatingFileHandler

formatter = logging.Formatter("[%(asctime)s] [%(pathname)s:%(lineno)d] %(levelname)s - %(message)s")
handler = RotatingFileHandler('log/main.log', maxBytes=1000000, backupCount=1)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(handler)

class QueryControler(object):
    def __init__(self,file_one):
        start = time.time()
        log.info("QC: entering init")
        self.model = SentenceTransformer("models/sts-GBERT-de")
        log.info("QC: ST model loaded")
        self.file_one=file_one
        self.embeddings2 =  self.model.encode(self.file_one.text, convert_to_tensor=True)
        log.info("QC: Embedggings encoded")
        self.ogd_selector=self.file_one.ogd==True
        end = time.time()
        time_elapsed=str(round(end-start,1))
        log.info("QC: INIT TIME "+time_elapsed)

    def lookup_query(self,query,ogd_check):
        log.info("QC: Query entered: "+query)
        start = time.time()
        if ogd_check:
            temp_embeddings=self.embeddings2[self.ogd_selector].detach().clone()
            temp_file_title=self.file_one.title[self.ogd_selector].copy()
        else:
            temp_embeddings=self.embeddings2
            temp_file_title=self.file_one.title
        embeddings1 = self.model.encode(query, convert_to_tensor=True)
        cosine_scores = util.pytorch_cos_sim(embeddings1, temp_embeddings)

        max_value = torch.max(cosine_scores)
        which=torch.argmax(cosine_scores)
        end = time.time()
        time_elapsed=str(round(end-start,1))
        #log.info(temp_file_title)
        #log.info(temp_file_title.shape)
        temp_which=temp_file_title.iloc[int(which)]
        #log.info(temp_which)
        return(str(temp_which)+" (Konfidenz in Match: "+str(int(100*max_value))+" %) gefunden in "+time_elapsed+" Sekunden.")


if __name__ == "__main__":
    temp=QueryControler(pd.read_csv("data.csv")[20:50])
    df = pd.read_csv("data.csv")[20:50]
    ogd_selector= df.ogd==True
    sub=temp.embeddings2[ogd_selector]
    sub=df.title[ogd_selector]
    print(sub.shape)
