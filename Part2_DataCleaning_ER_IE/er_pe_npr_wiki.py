from strsimpy.jaro_winkler import JaroWinkler
import pandas as pd


# Entity resolution - PE and NPR

npr=pd.read_csv('../Datasets/npr.csv')
pe=pd.read_csv('../Datasets/pe.csv')

pe["name"]=pe["name"].str.strip()

jarowinkler = JaroWinkler()
my_thres=0.69
list_id=[]
list_names=[]
dict_id={}
for i in range(len(npr)):
    for j in range(len(pe)):
        
        
        # if jarowinkler(npr.iloc[i,1],pe.iloc[j,1])>my_thres:
        t=(npr.iloc[i,0], pe.iloc[j,0])         
        ans=jarowinkler.similarity(npr.iloc[i,1],pe.iloc[j,1])
        if ans>my_thres:
            if npr.iloc[i,0] not in dict_id.keys():
                dict_id[npr.iloc[i,0]]=(pe.iloc[j,0],pe.iloc[j,1],ans)
                list_id.append(t)
                list_names.append((npr.iloc[i,1],pe.iloc[j,1]))
            elif ans>dict_id[npr.iloc[i,0]][-1]:
                list_id.remove((npr.iloc[i,0],dict_id[npr.iloc[i,0]][0]))
                list_names.remove((npr.iloc[i,1],dict_id[npr.iloc[i,0]][1]))
                dict_id[npr.iloc[i,0]]=(pe.iloc[j,0],pe.iloc[j,1],ans)
                list_id.append(t)
                list_names.append((npr.iloc[i,1],pe.iloc[j,1]))
            else:
                pass     



npr_list=[]
pe_list=[]
df_final=pd.DataFrame(columns=list(pe.columns)+list(npr.columns[-2:]))
for i,j in list_id:
    npr_list.append(i)
    pe_list.append(j)
    a=pe.iloc[j,:]
    b=npr.iloc[i,-2:]
    df_final=df_final.append(pd.concat([a,b]), ignore_index=True)


for i in range(len(pe)):
    if i not in pe_list:
        df_final=df_final.append(pe.iloc[i,:])

for i in range(len(npr)):
    if i not in npr_list:
        df_final=df_final.append(npr.iloc[i,:])
        
df_final["id"]=range(len(df_final))        




# Entity resolution - PE and NPR -> Wikidata

wikidata=pd.read_csv("../Datasets/wikidata.csv")
wikidata.rename(columns={"Unnamed: 0":"id"}, inplace=True)
wikidata['id']=range(len(wikidata))


jarowinkler = JaroWinkler()
my_thres=0.69
list_id=[]
list_names=[]
dict_id={}
for i in range(len(wikidata)):
    for j in range(len(df_final)):
        t=(wikidata.iloc[i,0], df_final.iloc[j,0])         
        ans=jarowinkler.similarity(wikidata.iloc[i,1],df_final.iloc[j,1])
        
        if ans>my_thres:
            if wikidata.iloc[i,0] not in dict_id.keys():
                dict_id[wikidata.iloc[i,0]]=(df_final.iloc[j,0],df_final.iloc[j,1],ans)
                list_id.append(t)
                list_names.append((wikidata.iloc[i,1],df_final.iloc[j,1]))
            elif ans>dict_id[wikidata.iloc[i,0]][-1]:
                list_id.remove((wikidata.iloc[i,0],dict_id[wikidata.iloc[i,0]][0]))
                list_names.remove((wikidata.iloc[i,1],dict_id[wikidata.iloc[i,0]][1]))
                dict_id[wikidata.iloc[i,0]]=(df_final.iloc[j,0],df_final.iloc[j,1],ans)
                list_id.append(t)
                list_names.append((wikidata.iloc[i,1],df_final.iloc[j,1]))
            else:
                pass     
        
        
  
        

df_final_list=[]
wikidata_list=[]
df_final1=pd.DataFrame(columns=list(df_final.columns)+list(wikidata.columns[-2:]))

for i,j in list_id:
    
    wikidata_list.append(i)
    df_final_list.append(j)
    a=df_final.iloc[j,:]
    b=wikidata.iloc[i,-2:]
    df_final1=df_final1.append(pd.concat([a,b]), ignore_index=True)


for i in range(len(df_final)):
    if i not in df_final_list:
        df_final1=df_final1.append(df_final.iloc[i,:])

for i in range(len(wikidata)):
    if i not in wikidata_list:
        df_final=df_final.append(wikidata.iloc[i,:])
        
df_final1["id"]=range(len(df_final1))               
           
        
df_final1.to_csv('../Datasets/er_pe_npr_wiki.csv', index=False)      
        
        
        
        
        
        
        
        
        
        