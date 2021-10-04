# WEBSITE - https://parksexpert.com/all-us-national-parks-list/

from bs4 import BeautifulSoup
import requests
import json
import pandas as pd


url = 'https://parksexpert.com/all-us-national-parks-list/'
page = requests.get(url)
f=open("../Datasets/pe.json","w")

soup = BeautifulSoup(page.content, 'html.parser')

   
        
np_tag=soup.find('div', class_="entry-content").find_all('h2')
np_list=[]
for n in np_tag:
    np_dict={}
    np_text=n.text.strip()
    if np_text[0].isnumeric():
        np_text=np_text[3:]
        if "," in np_text:
            np_dict["name"]=np_text.split(",")[0].strip()
            np_dict["state"]=np_text.split(",")[1].strip()
        else:
            np_dict["name"]=np_text
            np_dict["state"]=""
        np_list.append(np_dict)

            
   

tags=soup.find('div', class_="entry-content").find_all('p')
full_list=[]
tag_temp={}
for tag in tags:
    if tag.strong and tag.strong.text in ["Favorite Trails", "Must-Have Experience", "Scenic Drive", "Best Time to Go", "Admission Fee", "Where to Stay"]:
        # if tag.strong.text=="Where to Stay":
            # tag_temp[tag.strong.text]=tag.text.split(":")[1].strip().split(",")
        # else:
        tag_temp[tag.strong.text]=tag.text.split(":")[1].strip()
        if tag.strong.text=="Must-Have Experience":
            full_list.append(tag_temp)
            tag_temp={}
            

final_list=[]
for i,j in zip(np_list,full_list):
    final_list.append({**i,**j})
    # json.dump(np_dict, f, indent="") 

f.close()
 
    
df=pd.DataFrame(final_list)
df["id"]=df.index
cols=df.columns.tolist()
cols=[cols[-1]]+cols[:-1]
df=df[cols]
df.to_csv('../Datasets/pe.csv', index=False)
            
           
            
            
            