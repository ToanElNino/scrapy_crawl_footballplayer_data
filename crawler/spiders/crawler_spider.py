from scrapy import Spider
from scrapy.selector import Selector
from crawler.items import CrawlerItem
import scrapy
import json

class CrawlerSpider(Spider):
    name = "crawler"
    allowed_domains = ["fbref.com"]
    def start_requests(self):
        file = open('./link.json')
        urls = json.load(file)
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        questions = Selector(response).xpath('//div[@id="wrap"]')
        for question in questions:
            item = CrawlerItem()

            # player info
            if len(Selector(response).xpath('//div[@id="info"]//div[@id="meta"]//div[@class="nothumb"]')) == 0: 
                MediaItemSelector = Selector(response).xpath('//div[@id="info"]//div[@id="meta"]//div[2]')
                item['Name'] = MediaItemSelector.xpath('//h1//span/text()').extract_first()
                item['Birthday'] = MediaItemSelector.xpath('//p//span[@id="necro-birth"]/text()').extract_first()[5: -5]
            else :
                NothumbSelector = Selector(response).xpath('//div[@id="info"]//div[@id="meta"]//div[@class="nothumb"]')
                item['Name'] = NothumbSelector.xpath('//h1/span/text()').extract_first()
                item['Birthday'] = NothumbSelector.xpath('//span[@id="necro-birth"]/text()').extract_first()[5: -5]

            item['ClubCount'] = Selector(response).xpath('//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="team"]/text()').extract_first()[0:-5]
            item['LeagueCount'] = Selector(response).xpath('//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="comp_level"]/text()').extract_first()[0:-8]
            item['Game'] = Selector(response).xpath('//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="games"]/text()').extract_first()
            item['Goal'] = Selector(response).xpath('//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="goals"]/text()').extract_first()
            item['GoalPen'] = Selector(response).xpath('//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="goals_pens"]/text()').extract_first()
            item['Assist'] = Selector(response).xpath('//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="assists"]/text()').extract_first()
            item['YellowCard'] = Selector(response).xpath('//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="cards_yellow"]/text()').extract_first()
            item['RedCard'] = Selector(response).xpath('//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="cards_red"]/text()').extract_first()
            item['GoalPer90min'] = Selector(response).xpath('//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="goals_per90"]/text()').extract_first()
            item['AssistPer90min'] = Selector(response).xpath('//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="assists_per90"]/text()').extract_first()
            item['GAPer90min'] = Selector(response).xpath('//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="goals_assists_per90"]/text()').extract_first()
            yield item
