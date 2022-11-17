from scrapy import Spider
from scrapy.selector import Selector
from crawler.items import CrawlerItem
import scrapy
import re

class CrawlerSpider(Spider):
    name = "crawler"
    allowed_domains = ["fbref.com"]
    # start_urls = [
    #     "https://fbref.com/en/players/aa/",
    # ]
    def start_requests(self):
        urls = [
            'https://fbref.com/en/players/dea698d9/Cristiano-Ronaldo',
            'https://fbref.com/en/players/1f44ac21/Erling-Haaland',
            'https://fbref.com/en/players/d70ce98e/Lionel-Messi',
            'https://fbref.com/en/players/99127249/Antony',
            'https://fbref.com/en/players/e46012d4/Kevin-De-Bruyne',
            # 'https://fbref.com/en/players/9c60f681/Ahmad-Aadi',
            # 'https://fbref.com/en/players/ad713dff/Jamal-Aabbou'
            # 'https://fbref.com/en/players/ad713dff/Jamal-Aabbou',
            # 'https://fbref.com/en/players/c2e5d028/Zakariya-Aabbou',
            # 'https://fbref.com/en/players/c48b5529/Kim-Aabech',
            # 'https://fbref.com/en/players/d7ed844d/Kamilla-Aabel',
            # 'https://fbref.com/en/players/bb124176/Mohamed-Abd-El-Aal-Ali',
            # 'https://fbref.com/en/players/53ae3842/Nabil-Aankour',
            # 'https://fbref.com/en/players/e4b8c9c4/Edward-Aaron',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        questions = Selector(response).xpath('//div[@id="wrap"]')
        for question in questions:
            item = CrawlerItem()
            # player info
            if len(Selector(response).xpath('//div[@id="info"]//div[@id="meta"]//div[@class="nothumb"]')) == 0: 
            # item['Name'] = 'Ronaldo'
                MediaItemSelector = Selector(response).xpath('//div[@id="info"]//div[@id="meta"]//div[2]')
                item['Name'] = MediaItemSelector.xpath('//h1//span/text()').extract_first()
                # item['Heigh'] = MediaItemSelector.xpath('//p[3]//span[1]/text()').extract_first()[0:-2]
                # item['Weight'] = MediaItemSelector.xpath('//p[3]//span[2]/text()').extract_first()[0:-2]
                # item['National'] = MediaItemSelector.xpath('//p[5]/a/text()').extract_first()
                item['Birthday'] = MediaItemSelector.xpath('//p//span[@id="necro-birth"]/text()').extract_first()[5: -5]
            else :
                NothumbSelector = Selector(response).xpath('//div[@id="info"]//div[@id="meta"]//div[@class="nothumb"]')
                item['Name'] = NothumbSelector.xpath('//h1/span/text()').extract_first()
                item['Birthday'] = NothumbSelector.xpath('//span[@id="necro-birth"]/text()').extract_first()[5: -5]
                # item['Weight'] = ''
                # item['National'] = '...'
            # Table Stat
            # TableStatSelector = Selector(response).xpath('//div[@id="all_stats_standard"]//table/tfoot/tr[1]')   
            # item['Season'] = TableStatSelector('//th/text()').extract_first()[0:-6]
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
