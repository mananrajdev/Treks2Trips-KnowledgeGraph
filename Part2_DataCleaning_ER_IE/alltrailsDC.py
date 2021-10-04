import json_lines
import pandas as pd
import numpy as np


def cleaning_data():
    column_names = ['id', 'url', 'name', 'national_park', 'rating', 'difficulty', 'length', 'elevation_gain', 'route_type', 'no_shade', 'off_trail', 'scramble', 'over_grown', 'snow', 'bugs' ,'rocky', 'fee' ,'backpacking', 'bike_touring', 'bird_watching', 'camping', 'cross-country_skiing', 'fishing',  'hiking', 'horseback_riding', 'mountain_biking', 'nature_trips', 'ohv_offroad_driving', 'paddle_sports', 'road_biking', 'rock_climbing', 'scenic_driving', 'skiing', 'snowshoeing', 'running', 'via_ferrata', 'walking', 'beach', 'cave', 'city_walk', 'event', 'forest', 'historic_site', 'hot_springs', 'lake', 'pub_walk', 'rails_trails', 'river', 'views', 'waterfall', 'wildflowers', 'wildlife', 'dog_friendly', 'kid_friendly', 'paved', 'partially_paved', 'wheelchair_friendly', 'stroller_friendly', 'light', 'moderate', 'heavy']
    # print(len(column_names))
    # df = pd.DataFrame(columns = column_names)
    alltrails = []
    with open('../Datasets/alltrails.jl', 'rb') as f:
        trails = json_lines.reader(f)
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

            for x in item['attributes']:
                x = '_'.join(x.lower().split(' '))
                val = 1
                if x == 'ohv/off-road_driving':
                    x = 'ohv_offroad_driving'
                    

                if x == 'no_dogs':
                    x = 'dog_friendly'
                    val = 0
                
                if x == 'dogs_on_leash':
                    x = 'dog_friendly'

                if x in column_names:
                    item_dict[x] = val

            for col in column_names:
                if col not in item_dict:
                    item_dict[col] = 0
            
            # print(len(item_dict))
            alltrails.append(item_dict)

                # df.append(item_dict, ignore_index=True)
                # print(df.head(5))


    df = pd.DataFrame(alltrails, columns = column_names)
    df.to_csv('../Datasets/alltrails_cleaned.csv', index=False)
    print(len(alltrails))


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


if __name__ == "__main__":
    cleaning_data()
    columns = ['id', 'url', 'name', 'national_park', 'rating', 'difficulty', 'length', 'elevation_gain', 'route_type', 'no_shade', 'off_trail', 'scramble', 'over_grown', 'snow', 'bugs' ,'rocky', 'fee' ,'backpacking', 'bike_touring', 'bird_watching', 'camping', 'cross-country_skiing', 'fishing',  'hiking', 'horseback_riding', 'mountain_biking', 'nature_trips', 'ohv_offroad_driving', 'paddle_sports', 'road_biking', 'rock_climbing', 'scenic_driving', 'skiing', 'snowshoeing', 'running', 'via_ferrata', 'walking', 'beach', 'cave', 'city_walk', 'event', 'forest', 'historic_site', 'hot_springs', 'lake', 'pub_walk', 'rails_trails', 'river', 'views', 'waterfall', 'wildflowers', 'wildlife', 'dog_friendly', 'kid_friendly', 'paved', 'partially_paved', 'wheelchair_friendly', 'stroller_friendly', 'light', 'moderate', 'heavy']
    df = pd.read_csv('alltrails_cleaned.csv')[columns]
    # print(df.head(2))
    print(len(df))

    df2 = pd.read_csv('../Datasets/trek_url_list_info.csv', names=['name', 'state', 'time', 'url'], header=None).loc[:, ['name', 'state', 'time']]
    # print(df2.head(2))
    print(len(df2))

    merged = pd.merge(df, df2, on=['name'])
    
    merged['time'] = merged['time'].apply(time_decimal)

    merged.to_csv('../Datasets/alltrails_final.csv', index=False)
    print(merged.head(2))
    print(len(merged))
   


