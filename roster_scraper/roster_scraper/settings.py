# Scrapy settings for roster_scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'roster_scraper'

SPIDER_MODULES = ['roster_scraper.spiders']
NEWSPIDER_MODULE = 'roster_scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'roster_scraper (+http://www.yourdomain.com)'
