from scrapy.spider import Spider
from scrapy.selector import Selector

from roster_scraper.items import UncItem

class EspnSpider(Spider):
	name = 'unc'
	allowed_domains = ['espn.go.com']
	start_urls = [
		'http://espn.go.com/mens-college-basketball/team/stats/_/id/153/north-carolina-tar-heels'
	]

	def parse(self, response):
		sel = Selector(response)
		sites = sel.xpath('//table[1]/tr')
		items = []
		for site in sites:
			item = UncItem()
			item['name'] = site.xpath('td[1]/a/text()').extract()
			item['link'] = site.xpath('td[1]/a/@href').extract()
			item['ppg'] = site.xpath('td[4]/text()').extract()
			item['rpg'] = site.xpath('td[5]/text()').extract()
			item['apg'] = site.xpath('td[6]/text()').extract()
			item['spg'] = site.xpath('td[7]/text()').extract()
			item['bpg'] = site.xpath('td[8]/text()').extract()
			item['tpg'] = site.xpath('td[9]/text()').extract()
			item['fgp'] = site.xpath('td[10]/text()').extract()
			item['ftp'] = site.xpath('td[11]/text()').extract()
			item['tpp'] = site.xpath('td[12]/text()').extract()
			items.append(item)
		return items
