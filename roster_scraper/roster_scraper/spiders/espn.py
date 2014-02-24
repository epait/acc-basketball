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
		teams = sel.xpath('//table[1]/tr')
		items = []
		for team in teams:
			item = EspnItem()
			item['name'] = team.xpath('td[1]/a/text()').extract()
			item['link'] = team.xpath('td[1]/a/@href').extract()
			item['record'] = team.xpath('td[2]/text()').extract()
			items.append(item)
		return items
