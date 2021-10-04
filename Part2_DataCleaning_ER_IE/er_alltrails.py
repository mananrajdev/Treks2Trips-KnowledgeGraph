import pandas as pd
import jsonlines
import numpy as np

alltrails = []
with open('../Datasets/alltrails.jl', 'rb') as f:
    trails = jsonlines.Reader(f)
    for item in trails:
        item_dict = {}
        item_dict['id'] = item['Id']
        item_dict['url'] = item['url']
        item_dict['name'] = item['name']
        # item_dict['state'] = item['state']
        item_dict['national_park'] = item['national_park']
        item_dict['rating'] = float(item['rating'])
        item_dict['difficulty'] = item['difficulty']
        
        if 'Length' in item:
                item_dict['length'] = float(item['Length'][:-3].replace(',',''))
        else:
            item_dict['length'] = float(0)


        if 'Elevation gain' in item:
            item_dict['elevation_gain'] = float(item['Elevation gain'][:-3].replace(',',''))
        else:
            item_dict['elevation_gain'] = float(0)

        if 'Route type' in item:
            item_dict['route_type'] = item['Route type']
        else:
            item_dict['route_type'] = np.nan

        item['attributes']=list(map(str.lower,item['attributes']))
        
        if 'no dogs' in item['attributes']:
            item_dict["dog_status"]="No Dogs Allowed"
        elif 'dogs on leash' in item['attributes']:
            item_dict["dog_status"]="Dogs On Leash"
        else:
            item_dict["dog_status"]="No Restrictions"
            
        if ('kid friendly' in item['attributes']) or ('stroller friendly' in item['attributes']):
            item_dict["kid_status"]="Kid Friendly"
        else:
            item_dict["kid_status"]="Not Kid Friendly"
        
        if ('bike touring' in item['attributes']) or ('mountain biking' in item['attributes']) or ('road biking' in item['attributes']):
            item_dict["bike_status"]="Ideal For Biking"
        else:
            item_dict["bike_status"]="No Restrictions"
        
        
        item_dict["attributes"]=item['attributes']
       
        
        # print(len(item_dict))
        alltrails.append(item_dict)

df = pd.DataFrame(alltrails)

df2 = pd.read_csv('../Datasets/trek_url_list_info.csv', names=['name', 'state', 'time', 'url'], header=None).loc[:, ['name', 'state', 'time']]

merged = pd.merge(df, df2, on=['name'])
def time_decimal(time):
    # print('Before: ', time)
    if time != 'None' and 'Multi' not in time:
        time = time[:-2]
        if 'h' in time:
            lst = time.split(' h ')
            time = float(lst[0]) + float(lst[1])/60 
        else:
            time = float(time)/60 
        
    elif 'Multi' in time:
        time = 24
    else:
        time = 0

    # print('After: ', time)
    return round(float(time), 2)
  
merged['time'] = merged['time'].apply(time_decimal)

merged.to_csv('../Datasets/er_alltrails.csv', index=False)
