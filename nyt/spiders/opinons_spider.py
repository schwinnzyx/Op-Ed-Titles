
# Scrapy is an application framework for crawling web sites and extracting 
# structured data 
from scrapy import Spider
from scrapy.selector import Selector
from nyt.items import NytItem # class defined in items.py

class OpinionsSpider(Spider):
	# name my spider
	name = "opinions"
	
	# tell spider where to start
	start_urls = [
		"https://www.nytimes.com/section/opinion",
		#"https://www.foxnews.com/opinion",
	]

	# items to scrape
	def parse(self, response):
		# Selector concat is lit!
		source = Selector(response).css('title::text').extract_first()
		sec = Selector(response).css('h1[itemprop*="name"]::text').extract_first().strip()

		raw_headlines = Selector(response).css('a[data-rref]::text') \
		+ Selector(response).css('h2 a[href*="/2019"]::text') \
		+ Selector(response).css('h2.css-1dq8tca::text')

		headlines=list()
		# remove duplicates
		for headline in raw_headlines:
			if headline not in headlines:
				headlines.append(headline)
		
		for headline in headlines:
			item = NytItem()
			item['source'] = source
			item['headline'] = headline.extract()
			item['section']= sec
			yield item

	# improvement: need to detect and remove duplicates
'''
class ArtySpider(Spider):
	name = "arty"

	start_urls = [
		"https://www.nytimes.com/section/arts"
	]

	def parse(self, response):
		# Selector concat is lit!
		sec = Selector(response).css('h1.collection-heading::text').extract_first().strip()

		headlines = Selector(response).css('h2.headline a[href]::text')
		for headline in headlines:
			item = NytItem()
			item['headline'] = headline.extract()
			item['section']= sec
			yield item

'''