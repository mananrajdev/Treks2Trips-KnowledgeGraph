#run scrapy crawl alltrails -o alltrails.jl

import scrapy
import pandas as pd

class Alltrails_spider(scrapy.Spider):
    name = "alltrails"
    movies_list=[]
    # start_urls= ["https://www.alltrails.com/directory/trails/A/1"]
    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
        'CLOSESPIDER_ITEMCOUNT': 35001,
    }
    
    df=pd.read_csv("trek_url_list_info.csv", header=None)
    start_urls=list(df[3])
    
    def __init__(self):
        self.id=0
        
    def id_gen(self):
        self.id+=1
        return self.id
        
        
    def parse(self, response):
        if response:
            section_list=response.css('section.styles-module__trailStatSection___2PrNq span::text').getall()
            it = iter(section_list)
            section_dict = dict(zip(it, it))
            
            tag_cloud=response.css('section.tag-cloud span::text').getall()
            ans={
                # "Id": response.css('title::text').get().replace(' ',''),
                "Id" : str(self.id_gen()),
                "url": response.url,
                "name": response.css('h1.xlate-none.styles-module__name___1nEtW::text').get(default=''),
                "national_park":response.css('div.styles-module__content___1GUwP a::text').get(default='').strip(),
                "state": response.url.split("/")[-2],
                "rating":float(response.css('meta[itemprop=ratingValue]::attr(content)').get(default=0.0)),
                "difficulty" :response.css('span.styles-module__diff___22Qtv::text').get(default=''),
                "attributes":tag_cloud
                
            }
            
            ans.update(section_dict)
            yield ans
    
    

