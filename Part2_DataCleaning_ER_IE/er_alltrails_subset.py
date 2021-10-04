import pandas as pd

df_alltrails=pd.read_csv('../Datasets/er_alltrails.csv')
uniq_np_at=set(df_alltrails['national_park'].unique())
df_other3=pd.read_csv("../Datasets/er_other3.csv")
uniq_np_o3=set(df_other3['national_park'].unique())


diff=uniq_np_at.difference(uniq_np_o3)

for np in diff:
    df_alltrails.drop(df_alltrails.loc[df_alltrails['national_park']==np].index, inplace=True)

df_alltrails.to_csv('../Datasets/er_alltrails_subset.csv')
