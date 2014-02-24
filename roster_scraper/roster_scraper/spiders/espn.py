from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from roster_scraper.items import TeamItem, UncItem

class EspnSpider(Spider):
	name = 'acc_teams'
	allowed_domains = ['espn.go.com']
	start_urls = [
		'http://espn.go.com/mens-college-basketball/conferences/standings/_/id/2/acc-conference'
	]

	def parse(self, response):
		sel = Selector(response)
		teams = sel.xpath('//table[1]/tr')
		items = []
		for team in teams:
			item = TeamItem()
			item['name'] = team.xpath('td[1]/a/text()').extract()
			item['link'] = team.xpath('td[1]/a/@href').extract()
			item['record'] = team.xpath('td[2]/text()').extract()
			items.append(item)
		return items


class TeamSpider(Spider):
	name = 'unc_players'
	allowed_domains = ['espn.go.com']
	depth_limit = 15
	start_urls = [
		'http://espn.go.com/mens-college-basketball/team/stats/_/id/153/north-carolina-tar-heels'
	]

	def parse(self, response):
		sel = Selector(response)
		players = sel.xpath('//table[1]/tr')
		items = []
		for player in players:
			item = UncItem()
			item['name'] = player.xpath('td[1]/a/text()').extract()
			item['link'] = player.xpath('td[1]/a/@href').extract()
			item['ppg'] = player.xpath('td[4]/text()').extract()
			item['rpg'] = player.xpath('td[5]/text()').extract()
			item['apg'] = player.xpath('td[6]/text()').extract()
			item['spg'] = player.xpath('td[7]/text()').extract()
			item['bpg'] = player.xpath('td[8]/text()').extract()
			item['tpg'] = player.xpath('td[9]/text()').extract()
			item['fgp'] = player.xpath('td[10]/text()').extract()
			item['ftp'] = player.xpath('td[11]/text()').extract()
			item['tpp'] = player.xpath('td[12]/text()').extract()
			items.append(item)
		return items