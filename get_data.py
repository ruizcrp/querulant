





import pandas as pd
import json
from urllib.request import urlopen
import csv
import wget
import os
import io
import re

#import the central json file
orga="statistisches-amt-kanton-zuerich"
url="https://ckan.opendata.swiss/api/3/action/package_search?fq=organization:"+orga+"&rows=1000"
url="https://www.web.statistik.zh.ch/data/zhweb.json"
json_url = urlopen(url)
data = json.load(json_url)


identifiers=[]
titles=[]
texts=[]
ogd=[]

def pasteme(input1,input2):
    return str(input1)+" "+str(input2)


for i,entry in enumerate(data['dataset']):
    output=""
    print(i,":",entry['identifier']," ",entry['title'])
    output=pasteme(output,entry['title'])
    
    
    
    output=pasteme(output,entry['description'])



    temp_ogd=False
    for j,obj in enumerate(entry['keyword']):
        output=pasteme(output,obj)
        if(obj=="ogd"):
            temp_ogd=True


    for j,obj in enumerate(entry['theme']):
        output=pasteme(output,obj)
    
    print(output)
    identifiers.append(str(entry['identifier']))
    titles.append(str(entry['title']))
    texts.append(output)
    ogd.append(temp_ogd)
    
  
   
df = pd.DataFrame(zip(identifiers,titles,texts,ogd), columns=['identifier','title','text','ogd'])
df.to_csv('data.csv',index=False)
