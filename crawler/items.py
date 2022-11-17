import scrapy

class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    
    Name = scrapy.Field()
    # Position = scrapy.Field()
    Heigh = scrapy.Field()
    Weight = scrapy.Field()
    Birthday = scrapy.Field()
    National = scrapy.Field()
    # Salary= scrapy.Field()
    Season = scrapy.Field()
    ClubCount = scrapy.Field()
    LeagueCount = scrapy.Field()
    Game = scrapy.Field()
    Goal = scrapy.Field()
    GoalPen = scrapy.Field()
    Assist = scrapy.Field()
    YellowCard = scrapy.Field()
    RedCard = scrapy.Field()
    GoalPer90min = scrapy.Field()    
    AssistPer90min = scrapy.Field()
    GAPer90min = scrapy.Field()





