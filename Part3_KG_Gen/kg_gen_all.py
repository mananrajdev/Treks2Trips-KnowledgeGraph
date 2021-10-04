from rdflib import Graph, URIRef, Literal, XSD, Namespace, RDF
import pandas as pd
import numpy as np
import json
import ast


MYNS = Namespace('http://treks2trips.org/myfakenamespace#')
SCHEMA = Namespace('http://schema.org/')

my_kg = Graph()
my_kg.bind('myns', MYNS)
my_kg.bind('schema', SCHEMA)

df_other3=pd.read_csv("../Datasets/er_other3.csv")
df_struct=pd.read_csv("../Datasets/er_struct.csv")
df_alltrails=pd.read_csv("../Datasets/er_alltrails.csv")


trail_domain="http://treks2trips.org/trail/"
np_domain="http://treks2trips.org/nation_park/"
hotel_domain="http://treks2trips.org/hotel/"



# ----------------KG_GEN_OTHER3-----------------
for i in range(len(df_other3)):
    node_uri=URIRef(np_domain+df_other3.loc[i,"national_park"].lower().replace(" ","_"))
    my_kg.add((node_uri, RDF.type, SCHEMA.Park))
    my_kg.add((node_uri, SCHEMA.name, Literal(df_other3.loc[i,"national_park"])))
    my_kg.add((node_uri, SCHEMA.state, Literal(df_other3.loc[i,"state"])))
    if not pd.isna(df_other3.loc[i,"Scenic Drive"]):
        my_kg.add((node_uri, MYNS.scenic_drive, Literal(df_other3.loc[i,"Scenic Drive"])))
    
    if not pd.isna(df_other3.loc[i,"Best Time to Go"]):
        my_kg.add((node_uri, MYNS.best_time, Literal(df_other3.loc[i,"Best Time to Go"])))
        
    if not pd.isna(df_other3.loc[i,"Admission Fee"]):
        if df_other3.loc[i,"Admission Fee"]!="None":
            my_kg.add((node_uri, MYNS.fee, Literal(df_other3.loc[i,"Admission Fee"])))
        else:
            my_kg.add((node_uri, MYNS.fee, Literal("Free")))
    if pd.isna(df_other3.loc[i,"Admission Fee"]):
        my_kg.add((node_uri, MYNS.fee, Literal("Free")))
    
    if not pd.isna(df_other3.loc[i,"Must-Have Experience"]):
        my_kg.add((node_uri, MYNS.experience, Literal(df_other3.loc[i,"Must-Have Experience"])))
    
    if not pd.isna(df_other3.loc[i,"inception"]):
        my_kg.add((node_uri, MYNS.inception, Literal(df_other3.loc[i,"inception"], datatype=SCHEMA.Date)))
    
    if not pd.isna(df_other3.loc[i,"highest_peak"]):
        my_kg.add((node_uri, MYNS.highest_peak, Literal(df_other3.loc[i,"highest_peak"])))
    
    
    if not pd.isna(df_other3.loc[i,"hotel_name"]):
        hotels_list=ast.literal_eval(df_other3.loc[i,"hotel_name"])
        hotels_list = list(map(str.strip, hotels_list))
        hotels_price=ast.literal_eval(df_other3.loc[i,"hotel_price"])
        for h in range(len(hotels_list)):
            hotel_uri=URIRef(hotel_domain+hotels_list[h].lower().replace(" ","_"))
            my_kg.add((hotel_uri, RDF.type, SCHEMA.Hotel))
            my_kg.add((hotel_uri, SCHEMA.name, Literal(hotels_list[h])))
            my_kg.add((hotel_uri, SCHEMA.price, Literal(hotels_price[h], datatype=SCHEMA.Float)))
            my_kg.add((node_uri, MYNS.has_hotel, hotel_uri))
            
    if pd.isna(df_other3.loc[i,"hotel_name"]) and not pd.isna(df_other3.loc[i,"Where to Stay"]):
        hotels_list=df_other3.loc[i,"Where to Stay"].split(",")
        hotels_list = list(map(str.strip, hotels_list))
        for h in range(len(hotels_list)):
            hotel_uri=URIRef(hotel_domain+hotels_list[h].lower().replace(" ","_"))
            my_kg.add((hotel_uri, RDF.type, SCHEMA.Hotel))
            my_kg.add((hotel_uri, SCHEMA.name, Literal(hotels_list[h])))
            
        
        



# ----------------KG_GEN_STRUCT-----------------
for i in range(len(df_struct)):
    node_uri=URIRef(np_domain+df_struct.loc[i,"national_park"].lower().replace(" ","_"))
    my_kg.add((node_uri, RDF.type, SCHEMA.Park))
    my_kg.add((node_uri, SCHEMA.name, Literal(df_struct.loc[i,"national_park"])))
    my_kg.add((node_uri, MYNS.species, Literal(df_struct.loc[i,"Common Names"])))
    
        

        
# ----------------KG_GEN_ALLTRAILS-----------------
for i in range(len(df_alltrails)):
    node_uri=URIRef(trail_domain+df_alltrails.loc[i,"url"][35:-16])
    np_uri=URIRef(np_domain+df_alltrails.loc[i,"national_park"].lower().replace(" ","_").replace('"',''))
    my_kg.add((node_uri, RDF.type, MYNS['Trail'])) 
    my_kg.add((node_uri, SCHEMA.name, Literal(df_alltrails.loc[i,"name"])))
    my_kg.add((node_uri, MYNS.national_park, np_uri))
    my_kg.add((node_uri, SCHEMA.state, Literal(df_alltrails.loc[i,"state"])))
    my_kg.add((node_uri, SCHEMA.ratingValue, Literal(df_alltrails.loc[i,"rating"], datatype=SCHEMA.Float)))
    my_kg.add((node_uri, MYNS.difficulty, Literal(df_alltrails.loc[i,"difficulty"])))
    my_kg.add((node_uri, SCHEMA.distance, Literal(df_alltrails.loc[i,"length"], datatype=SCHEMA.Float)))
    my_kg.add((node_uri, SCHEMA.duration, Literal(df_alltrails.loc[i,"time"], datatype=SCHEMA.Float)))
    my_kg.add((node_uri, SCHEMA.elevation, Literal(df_alltrails.loc[i,"elevation_gain"], datatype=SCHEMA.Integer)))
    my_kg.add((node_uri, MYNS.route_type, Literal(df_alltrails.loc[i,"route_type"])))
    my_kg.add((node_uri, MYNS.dog_status, Literal(df_alltrails.loc[i,"dog_status"])))
    my_kg.add((node_uri, MYNS.kid_status, Literal(df_alltrails.loc[i,"kid_status"])))
    my_kg.add((node_uri, MYNS.bike_status, Literal(df_alltrails.loc[i,"bike_status"])))
    attribute_list=df_alltrails.loc[i,"attributes"].strip('][').split(', ')
    
    for e in attribute_list:
       my_kg.add((node_uri, MYNS.attributes, Literal(e.replace("'","").strip()))) 

    
# ----------------SAVE FILE-----------------
my_kg.serialize('../Datasets/KG_final_triples.ttl', format="turtle")
