from scrapy import Spider, Request
from scrapy.selector import Selector
from crawler.items import CrawlerItem
import json
import time


class CrawlerSpider(Spider):
    name = "crawler"
    allowed_domains = ["fbref.com"]

    def start_requests(self):
        with open(f"/root/scrapy-{self.range}/link{self.range}.json") as f:
            objects = json.load(f)
            
        for i in objects:
            yield Request(url=f"https://fbref.com{i['Link']}", callback=self.parse)
            time.sleep(10)
        f.close()

    def parse(self, response):
        questions = Selector(response).xpath('//div[@id="wrap"]')
        print("ahihi", questions)
        for question in questions:
            item = CrawlerItem()
            # player info
            if len(Selector(response).xpath('//div[@id="info"]//div[@id="meta"]//div[@class="nothumb"]')) == 0:
                item['Name'] = Selector(response).xpath(
                    '//div[@id="info"]//div[@id="meta"]//div[2]//h1//span/text()').extract_first()
                # item['Name'] = data[0]
                infoList = Selector(response).xpath(
                    '//div[@id="info"]//div[@id="meta"]//div[2]//p')
                for x in range(len(infoList)):
                    pathSpan = '//div[@id="info"]//div[@id="meta"]//div[2]//p[' + \
                        str(x+1) + ']//span/text()'
                    pathStrong = '//div[@id="info"]//div[@id="meta"]//div[2]//p[' + \
                        str(x+1) + ']//strong/text()'
                    # Heigh
                    if len(Selector(response).xpath(pathStrong)) > 0:
                        if Selector(response).xpath(pathStrong).extract_first()[-2:] == 'cm':
                            item['Heigh'] = Selector(response).xpath(
                                pathStrong).extract_first()[0:-2]
                        if Selector(response).xpath(pathStrong).extract_first() == 'National Team:':
                            patha = '//div[@id="info"]//div[@id="meta"]//div[2]//p[' + \
                                str(x+1) + ']//a/text()'
                            item['National'] = Selector(
                                response).xpath(patha).extract_first()
                        if Selector(response).xpath(pathStrong).extract_first() == 'Club:':
                            patha = '//div[@id="info"]//div[@id="meta"]//div[2]//p[' + \
                                str(x+1) + ']//a/text()'
                            item['Club'] = Selector(response).xpath(
                                patha).extract_first()
                    if len(Selector(response).xpath(pathSpan)) > 0:
                        if Selector(response).xpath(pathSpan).extract_first()[-2:] == 'cm':
                            item['Heigh'] = Selector(response).xpath(
                                pathSpan).extract_first()[0:-2]
                    # National

            else:
                NothumbSelector = Selector(response).xpath(
                    '//div[@id="info"]//div[@id="meta"]//div[@class="nothumb"]')
                item['Name'] = NothumbSelector.xpath(
                    '//h1/span/text()').extract_first()
                item['Birthday'] = NothumbSelector.xpath(
                    '//span[@id="necro-birth"]/text()').extract_first()[5: -5]
                infoList = Selector(response).xpath(
                    '//div[@id="info"]//div[@id="meta"]//div[@class="nothumb"]/p')
                for x in range(len(infoList)):
                    pathSpan = '//div[@id="info"]//div[@id="meta"]//div[@class="nothumb"]//p[' + str(
                        x+1) + ']//span/text()'
                    pathStrong = '//div[@id="info"]//div[@id="meta"]//div[@class="nothumb"]//p[' + str(
                        x+1) + ']//strong/text()'
                    # Heigh
                    if len(Selector(response).xpath(pathStrong)) > 0:
                        if Selector(response).xpath(pathStrong).extract_first()[-2:] == 'cm':
                            item['Heigh'] = Selector(response).xpath(
                                pathStrong).extract_first()[0:-2]
                        if Selector(response).xpath(pathStrong).extract_first() == 'National Team:':
                            patha = '//div[@id="info"]//div[@id="meta"]//div[@class="nothumb"]//p[' + str(
                                x+1) + ']//a/text()'
                            item['National'] = Selector(
                                response).xpath(patha).extract_first()
                        if Selector(response).xpath(pathStrong).extract_first() == 'Club:':
                            patha = '//div[@id="info"]//div[@id="meta"]//div[@class="nothumb"]//p[' + str(
                                x+1) + ']//a/text()'
                            item['Club'] = Selector(response).xpath(
                                patha).extract_first()
                    if len(Selector(response).xpath(pathSpan)) > 0:
                        if Selector(response).xpath(pathSpan).extract_first()[-2:] == 'cm':
                            item['Heigh'] = Selector(response).xpath(
                                pathSpan).extract_first()[0:-2]

            item['ClubCount'] = Selector(response).xpath(
                '//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="team"]/text()').extract_first()[0:-5]
            item['LeagueCount'] = Selector(response).xpath(
                '//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="comp_level"]/text()').extract_first()[0:-8]
            item['Game'] = Selector(response).xpath(
                '//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="games"]/text()').extract_first()
            item['Goal'] = Selector(response).xpath(
                '//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="goals"]/text()').extract_first()
            item['GoalPen'] = Selector(response).xpath(
                '//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="goals_pens"]/text()').extract_first()
            item['Assist'] = Selector(response).xpath(
                '//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="assists"]/text()').extract_first()
            item['YellowCard'] = Selector(response).xpath(
                '//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="cards_yellow"]/text()').extract_first()
            item['RedCard'] = Selector(response).xpath(
                '//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="cards_red"]/text()').extract_first()
            item['GoalPer90min'] = Selector(response).xpath(
                '//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="goals_per90"]/text()').extract_first()
            item['AssistPer90min'] = Selector(response).xpath(
                '//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="assists_per90"]/text()').extract_first()
            item['GAPer90min'] = Selector(response).xpath(
                '//div[@id="all_stats_standard"]//table/tfoot/tr[1]//td[@data-stat="goals_assists_per90"]/text()').extract_first()
            yield item
