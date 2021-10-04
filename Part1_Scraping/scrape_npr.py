from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

url = 'https://www.nationalparkreservations.com/'
page = requests.get(url)
f=open("../Datasets/npr.json","w")

soup = BeautifulSoup(page.content, 'html.parser')

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

final_list=[]
for np in soup.find_all('div', class_="content-box left-position park-data"):
    np_dict={}
    np_dict["name"]=np.find('h4', class_='park-name').text.strip()
    np_dict["state"]=np.find('h5', class_='state-location').text.strip()
    url2=np.find('a', class_="green-button")['href']+"lodges/"
    page2=requests.get(url2)
    soup2=BeautifulSoup(page2.content, 'html.parser')
    np_hotels_name=[]
    np_hotels_price=[]
    for h in soup2.find_all('div', class_="content-box box-lodge clearfix"):
        name=h.find('a').text.strip()[3:]
        price=h.find('span').text.strip()[1:]
        if isfloat(price):
            price=float(price)
        else:
            continue
        link=h.find('a')['href']
        np_hotels_name.append(name)
        np_hotels_price.append(price)
    np_dict["hotel_name"]=np_hotels_name
    np_dict["hotel_price"]=np_hotels_price
    final_list.append(np_dict)
    json.dump(np_dict, f, indent="")    
    
f.close()


df=pd.DataFrame(final_list)
df["id"]=df.index
cols=df.columns.tolist()
cols=[cols[-1]]+cols[:-1]
df=df[cols]
df.to_csv('../Datasets/npr.csv', index=False)



