import pandas as pd
from strsimpy.jaro_winkler import JaroWinkler
jarowinkler = JaroWinkler()

df_species=pd.read_csv('../Datasets/species.csv', usecols=['Park Name', 'Common Names', 'Category', 'Occurrence', 'Record Status'])

# -----------STRUCTURED DATA PREPROCESSING--------------
df_species=df_species[df_species["Record Status"]=="Approved"]
df_species=df_species[df_species["Occurrence"]=="Present"]

df_species['Common Names']=df_species['Common Names'].str.split(",")
df_species['Common Names']= df_species['Common Names'].map(lambda x: sorted(list(x))[0].strip())




df_species.loc[df_species['Common Names'].str.split().str.len() > 1, 'Common Names'] = df_species['Common Names'].str.split().str[-1]

df_species.drop_duplicates(inplace=True)










uniq_np_sp=set(df_species['Park Name'].unique())

df_final=pd.read_csv('../Datasets/er_alltrails.csv')
uniq_np_fin=set(df_final['national_park'].unique())

intersec=uniq_np_sp.intersection(uniq_np_fin)

diff=uniq_np_sp.difference(intersec)

# df_species['Park Name'].replace("Sequoia and Kings Canyon National Parks", "Sequoia National Park", inplace=True)
# a=sorted(uniq_np_fin)
# df_species['Park Name'].replace("Katmai National Park and Preserve", "Katmai National Park", inplace=True)

df_species['Park Name'].replace("Wrangell - St Elias National Park and Preserve", "Wrangell–St. Elias National Park and Preserve", inplace=True)

# df_species['Park Name'].replace("Denali National Park and Preserve", "Denali National Park, Alaska", inplace=True)


# -------ENTITY RESOLUTION-----------
er_dict={}
for i in list(diff):
    pn=i.split()[0]
    for j in list(df_final['national_park'].unique()):
        if pn==j.split()[0]: #BLOCKING
            sim=jarowinkler.similarity(i,j)
            if i not in er_dict.keys():
                er_dict[i]=(j,sim)
            elif er_dict[i][1]<sim:
                er_dict[i]=(j,sim)
            
my_thres=0.8                      
for key, value in er_dict.items():
    if value[1]>my_thres:
        df_species['Park Name'].replace(key,value[0], inplace=True)


# REMOVING THOSE NP NOT IN ALLTRAILS
for np in diff:
    df_species.drop(df_species.loc[df_species['Park Name']==np].index, inplace=True)

df_species.rename(columns={"Park Name":"national_park"}, inplace=True)




df_species.reset_index(inplace=True)
df_species.drop('index', axis=1, inplace=True)

df_species.to_csv('../Datasets/er_struct.csv', index=False)                 
