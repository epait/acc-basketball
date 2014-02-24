# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class EspnItem(Item):
    name = Field()
    link = Field()
    record = Field()

class UncItem(Item):
	name = Field()
	link = Field()
	ppg = Field()
	rpg = Field()
	apg = Field()
	spg = Field()
	bpg = Field()
	tpg = Field()
	fgp = Field()
	ftp = Field()
	tpp = Field()
