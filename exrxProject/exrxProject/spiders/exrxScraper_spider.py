from scrapy.spider import Spider
from scrapy.selector import Selector
from exrxProject.items import ExrxItem
#scrapy crawl exrx -o items.csv -t csv

class exrxScraperSpider(Spider):
    name = "exrx"
    allowed_domains = ["exrx.net"]
    start_urls = [
            "http://www.exrx.net/Lists/Directory.html",
            ]

    def parse(self, response):

    	sel = Selector(response)
    	sites = sel.xpath('//ul/li')
        exerciseTable = sel.xpath('//h2[contains(text(), "Exercises")]')

    	items = []

    	for site in exerciseTable:
    		item = ExrxItem()

                item['exerciseCategory'] = exerciseTable.xpath('../ul/li/a/text()').extract()
    		#item['exerciseCategory'] = site.xpath('a/text()').extract()
    		#item['exerciseCategory'] = site.xpath('[re:test(text(), "\S+"]').re(r'\S+')

    		#item['exerciseCategory'] = site.re(r'./li \S+')
    		#item['exerciseCategory'] = site.xpath('[re:test(text(), "\S")]').extract()
    		#title = site.xpath('a/text()').extract()
    		#item['title'] = title
    		#link = site.xpath('a/@href').extract()
    		#item['link'] = link
    		#print title, link, desc
    		items.append(item)
    	return items
