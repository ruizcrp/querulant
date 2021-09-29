import streamlit as st
import pandas as pd
import numpy as np
import string
import torch as torch
import time

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('Sahajtomar/sts-GBERT-de')

file_one=pd.read_csv("data.csv")
st.session_state.embeddings2 =  model.encode(file_one.text, convert_to_tensor=True)

def lookup_query(query,embeddings2):
    start = time.time()
    embeddings1 = model.encode(query, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)
    #print(cosine_scores)

    max_value = torch.max(cosine_scores)
    print(max_value)
    which=torch.argmax(cosine_scores)
    print(which)
    end = time.time()
    time_elapsed=str(round(end-start,1))
    return(str(file_one.title[int(which)])+" ("+str(int(100*max_value))+" perc) gefunden in "+time_elapsed+" Sekunden")


st.title('Querulant')

user_input = st.text_input("Suchbegriff eingeben:")
if(user_input!=""):
    result=lookup_query(user_input,st.session_state.embeddings2)
    st.write(result)
