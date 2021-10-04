# TODO: ADD YOUR DISTANT SUPERVISION LABELING FUNCTIONS AND ANSWER TASK 3 QUESTIONS
# !pip install SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>

Select ?np ?npLabel ?inception ?hpLabel  where {
?np wdt:P31 wd:Q34918903 ;
  wdt:P571 ?inception ;
    wdt:P610 ?hp .
#     wdt:P527 ?haspart ;


SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
   }
}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()



results_df = pd.io.json.json_normalize(results['results']['bindings'])
results_df1=results_df[["npLabel.value", "inception.value","hpLabel.value"]]
results_df1=results_df1.drop_duplicates(subset=["npLabel.value"])
results_df1.rename(columns={"npLabel.value":"name", "inception.value":"inception","hpLabel.value":"highest_peak"}, inplace=True)

results_df1.to_csv("../Datasets/wikidata.csv")
