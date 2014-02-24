from scrapy.spider import Spider
from scrapy.selector import Selector

from roster_scraper.items import EspnItem

class EspnSpider(Spider):
	name = 'espn'
	allowed_domains = ['espn.go.com']
	start_urls = [
		'http://espn.go.com/mens-college-basketball/conferences/standings/_/id/2/acc-conference'
	]

	def parse(self, response):
		sel = Selector(response)
		sites = sel.xpath('//table[1]/tr')
		items = []
		for site in sites:
			item = EspnItem()
			item['name'] = site.xpath('td[1]/a/text()').extract()
			item['link'] = site.xpath('td[1]/a/@href').extract()
			item['record'] = site.xpath('td[2]/text()').extract()
			items.append(item)
		return items
