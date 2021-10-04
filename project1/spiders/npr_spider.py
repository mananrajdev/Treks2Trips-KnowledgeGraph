#run scrapy crawl alltrails -o Manan_Rajdev_hw01_movies.jl

import scrapy
import json
# from datetime import datetime

class Npr_spider(scrapy.Spider):
    name = "npr"
    np_list=[]
    start_urls= ["https://www.nationalparkreservations.com/"]
    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
        'CLOSESPIDER_ITEMCOUNT': 5001,
    }
    f=open("npr.json","w")
    def __init__(self):
        self.id=0
        
    def id_gen(self):
        self.id+=1
        return self.id
        
        
    def parse(self, response):
        if response:
            np_dict={}
            for np in response.css("div.content-box.left-position.park-data"):
                np_dict["name"]=np.css('h4.park-name::text').get(default='').strip()
                np_dict["state"]=np.css('h5.state-location::text').get(default='').strip()
                np_url= np.css("a.green-button::attr(href)").get()
                
                if np_url:
                    np_url+="lodges/"
                    yield scrapy.Request(np_url, callback=self.parse2)
                
                
                
                
            # next_page = response.css('a.action[rel=next]::attr(href)').get()
            # if next_page:
            #     yield response.follow(url=response.urljoin(next_page), callback=self.parse)
            
    def parse2(self, response):
        if response:
            np_hotel=response.css("div.content-box.box-lodge.clearfix")
            np_hotel_list=[]
            
            for h in np_hotel:
                np_hotel_dict={}
                np_hotel_dict["hotel_name"]=h.css("a::text").get(default='').strip()
                np_hotel_dict["hotel_price"]=h.css("span::text").get(default='').strip()[1:]
                np_hotel_dict["hotel_link"]=h.css("a::attr(href)").get(default='').strip()
                np_hotel_list.append(np_hotel_dict)
                
            self.np_dict["hotels"]= np_hotel_list
            json.dump(self.np_dict,self.f, indent="")
           
        # yield{
        #         # "Id": response.css('title::text').get().replace(' ',''),
        #         "Id" : str(self.id_gen()),
        #         "url": response.url,
        #         "timestamp_crawl": datetime.now().isoformat(),
        #         "title": response.css('h1[itemprop=name]::text').get(default=''),
        #         "contact_info": response.css('p[id=text-container-contact_info]::text').get(default='')
                
        #     }
            
           
