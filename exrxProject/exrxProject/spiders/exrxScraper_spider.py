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

    def getEquipmentName(self, sel):
        count = 0
        parentName = sel.xpath('../text()').extract()
        return sel.xpath('.//ancestor::*[contains(text(), "Barbell")]').extract()

    def parseCategory(self, response):
        sel = Selector(response)
        sites = sel.xpath('//ul/li/a')
        for sel in sites:
            validLinks = sel.xpath('./@href[contains(., "WeightExercises") \
                            or contains(., "Plyometrics") \
                            or contains(., "Stretches")]')
            links = validLinks.extract()
            link = ''
            title = ''


            titleList = validLinks.xpath('./text()').extract()
            if titleList == []:
                titleList = sel.xpath('./i/text()').extract()
            newTitleList = [re.sub(r'\r\n\s*', ' ', title).replace('\n', ' ').replace('\r', ' ') for title in titleList]
            for s in newTitleList:
                title = s
            for s in links:
                link = 'www.exrx.net/' + s.replace('../../','' )
                
            if (not (link == '')) and (not (title == '')):
                item = ExrxCategory()
                item['link'] = link
                item['title'] = title
                yield item 

    def parse(self, response):
        sel = Selector(response)
        exercises = sel.xpath('//h2[contains(text(), "Exercises")]')
        sites = exercises.xpath('./..//ul//li')
        items = []
        for sel in sites:
            link = sel.xpath('./a/@href').extract()
            for s in link:
                req = Request('http://www.exrx.net/Lists/' + s, callback=self.parseCategory)
                yield req

