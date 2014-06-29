from scrapy.spider import Spider
from scrapy.selector import Selector
from exrxProject.items import ExrxItem, ExrxCategory, ExrxExercise
from scrapy.http import Request
import re


#TO OUTPUT TO JSON RUN THIS COMMAND
#run in dir: exrxScraper/exrxProject
#scrapy crawl exrx -o items.json -t json 

class exrxScraperSpider(Spider):
    name = "exrx"
    allowed_domains = ["exrx.net"]
    start_urls = [
            "http://www.exrx.net/Lists/Directory.html",
            ]

    def parseExercise(self, response):
        sel = Selector(response)
        exerciseItems = []

        instructionsTree = sel.xpath('//h2[contains(text(), "Instructions")]')
        print instructionsTree
        item = ExrxExercise()
        prep = instructionsTree.xpath('./../dl/dd[contains(text(), "Preparation")]')
        item['preparation'] = prep.xpath('./text()').extract()
        execution = instructionsTree.xpath('./../dl/dd[contains(text(), "Execution")]')
        item['execution'] = execution.xpath('./text()').extract()
        exerciseItems.append(item)
        yield item 

    def parseCategory(self, response):
        sel = Selector(response)
        sites = sel.xpath('//ul/li/a')
        for sel in sites:
            item = ExrxCategory()
            link = sel.xpath('./@href').extract()

            titleList = sel.xpath('./text()').extract()
            if titleList == []:
                titleList = sel.xpath('./i/text()').extract()
            newTitleList = [re.sub(r'\r\n\s*', ' ', title) for title in titleList]

            equipmentDict = {}

            item['title'] = newTitleList
            item['link'] = link
            """
            for s in link:
                print s
                print response.url
                req = Request(response.url + "/" + s, callback=self.parseExercise)
                yield req
            """
            yield item 

    def parse(self, response):

        sel = Selector(response)
        exercises = sel.xpath('//h2[contains(text(), "Exercises")]')
        print exercises
        print exercises.xpath('./text()').extract()
        sites = exercises.xpath('./..//ul//li')
        items = []
        print sites
        for sel in sites:
            item = ExrxItem()
            link = sel.xpath('./a/@href').extract()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = link
            for s in link:
                req = Request('http://www.exrx.net/Lists/' + s, callback=self.parseCategory)
                yield req
            items.append(item)
            #yield item

