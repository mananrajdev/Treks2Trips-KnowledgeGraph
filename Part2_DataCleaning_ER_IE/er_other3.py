import pandas as pd
from strsimpy.jaro_winkler import JaroWinkler
jarowinkler = JaroWinkler()

df_alltrails=pd.read_csv('../Datasets/er_alltrails.csv')
uniq_np_at=set(df_alltrails['national_park'].unique())




df_other3=pd.read_csv("../Datasets/er_pe_npr_wiki.csv")

# ER sequoia
df_other3.loc[1,"hotel_name"]=df_other3[df_other3['id']==63]['hotel_name'].values
df_other3.loc[1,"hotel_price"]=df_other3[df_other3['id']==63]['hotel_price'].values
df_other3.loc[35,"hotel_name"]=df_other3[df_other3['id']==63]['hotel_name'].values
df_other3.loc[35,"hotel_price"]=df_other3[df_other3['id']==63]['hotel_price'].values
df_other3.drop(63, axis=0, inplace=True)

# ER arches
df_other3.loc[23,"hotel_name"]=df_other3[df_other3['id']==64]['hotel_name'].values
df_other3.loc[23,"hotel_price"]=df_other3[df_other3['id']==64]['hotel_price'].values
df_other3.loc[9,"hotel_name"]=df_other3[df_other3['id']==64]['hotel_name'].values
df_other3.loc[9,"hotel_price"]=df_other3[df_other3['id']==64]['hotel_price'].values
df_other3.drop(64, axis=0, inplace=True)

# ER wrangel
df_other3['name'].replace("Wrangell-St.Elias National Park", "Wrangell–St. Elias National Park and Preserve", inplace=True)



uniq_np_o3=set(df_other3['name'].unique())




intersec=uniq_np_o3.intersection(uniq_np_at)

diff=uniq_np_o3.difference(intersec)

er_dict={}
for i in list(diff):
    pn=i.split()[0]
    for j in list(uniq_np_at):
        if pn==j.split()[0]: #BLOCKING
            sim=jarowinkler.similarity(i,j)
            if i not in er_dict.keys():
                er_dict[i]=(j,sim)
            elif er_dict[i][1]<sim:
                er_dict[i]=(j,sim)
            
my_thres=0.89                   
for key, value in er_dict.items():
    if value[1]>my_thres:
        df_other3['name'].replace(key,value[0], inplace=True)
        diff.remove(key)



# REMOVING THOSE NP NOT IN ALLTRAILS
for np in diff:
    df_other3.drop(df_other3.loc[df_other3['name']==np].index, inplace=True)

df_other3.rename(columns={"name":"national_park"}, inplace=True)

#State spelling ER
df_other3['state'].replace('Tennesse', 'Tennessee', inplace=True)


df_other3.reset_index(inplace=True)
df_other3.drop('index', axis=1, inplace=True)





df_other3['id']=range(len(df_other3))                  
df_other3.to_csv('../Datasets/er_other3.csv', index=False)   







# EXTRA


# a=pd.DataFrame(df_alltrails['national_park'].value_counts())
# a.reset_index(inplace=True)
# a.rename(columns={'index':'name'}, inplace=True)


# a['np']=list(a['name'].str.contains('National Park'))
# a=sorted(uniq_np_o3)
# b=a[a['np']==True]
# b['id']=range(len(b))
# b=b[['id','name']]

# jarowinkler = JaroWinkler()
# my_thres=0.69
# list_id=[]
# list_names=[]
# dict_id={}

# wikidata=b
# df_final=df_other

# for i in range(len(wikidata)):
#     for j in range(len(df_final)):
#         t=(wikidata.iloc[i,0], df_final.iloc[j,0])         
#         ans=jarowinkler.similarity(wikidata.iloc[i,1],df_final.iloc[j,1])
        
#         if ans>my_thres:
#             if wikidata.iloc[i,0] not in dict_id.keys():
#                 dict_id[wikidata.iloc[i,0]]=(df_final.iloc[j,0],df_final.iloc[j,1],ans)
#                 list_id.append(t)
#                 list_names.append((wikidata.iloc[i,1],df_final.iloc[j,1]))
#             elif ans>dict_id[wikidata.iloc[i,0]][-1]:
#                 list_id.remove((wikidata.iloc[i,0],dict_id[wikidata.iloc[i,0]][0]))
#                 list_names.remove((wikidata.iloc[i,1],dict_id[wikidata.iloc[i,0]][1]))
#                 dict_id[wikidata.iloc[i,0]]=(df_final.iloc[j,0],df_final.iloc[j,1],ans)
#                 list_id.append(t)
#                 list_names.append((wikidata.iloc[i,1],df_final.iloc[j,1]))
#             else:
#                 pass     
