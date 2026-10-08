import scrapy
from ..items import PoliticscrawlerItem
from news.models import PHeadline
from politicscrawler.spiders import politics_spider
from politicscrawler import pipelines

class PoliticsSpider(scrapy.Spider):
	name = "politics"
	start_urls = [
		'https://www.nytimes.com/section/politics'
	]

	def parse(self, response):
		


		#div_all_news = response.xpath("//div[@class='css-13mho3u']/ol/li/div/div")
	
		for i in range(10):
			items = PoliticscrawlerItem()
			title = response.xpath("//div[@class='css-13mho3u']/ol/li/div/div/a/h2/text()")[i].extract()
			link = "https://www.nytimes.com" + response.xpath("//div[@class='css-13mho3u']/ol/li/div/div/a/@href")[i].extract()
			img = response.xpath("//div[@class='css-13mho3u']/ol/li/div/div/a/div[@class='css-79elbk']/figure/@itemid")[i].extract()
			items["title"] = title
			items["image"] = img
			items["url"] = link
			items['source'] = 'New York Times'
			yield items
			

class EconomicSpider(scrapy.Spider):
	name = "ecopolitics"
	start_urls = [
		'https://economictimes.indiatimes.com/news/politics-nation?from=mdr'
	]

	def parse(self, response):
		


		for i in range(10):
			items = PoliticscrawlerItem()
			title = response.xpath("//section[@id='bottomContent']/section/div/h3/a/text()")[i].extract()
			link = "https://economictimes.indiatimes.com" + response.xpath("//section[@id='bottomContent']/section/div/a/@href")[i].extract()
			img = response.xpath("//section[@id='bottomContent']/section/div/a/span/img/@data-original")[i].extract()
			items["title"] = title
			items["image"] = img
			items["url"] = link
			items['source'] = 'Economic Times'
			yield items

class TimesOfIndiaPoliticsSpider(scrapy.Spider):
	name = "toipolitics"
	start_urls = [
		'https://timesofindia.indiatimes.com/politics'
	]

	def parse(self, response):
		articles = response.xpath("//div[@class='uwU81']")
		for article in articles[:12]:  # Limit to 12 articles
			items = PoliticscrawlerItem()
			title = article.xpath(".//span[@class='w_tle']/text()").get()
			link = article.xpath(".//a/@href").get()
			img = article.xpath(".//img/@src").get()
			
			if title and link:
				if not link.startswith('http'):
					link = 'https://timesofindia.indiatimes.com' + link
				
				items['title'] = title.strip()
				items['image'] = img if img else ''
				items['url'] = link
				items['source'] = 'Times of India'
				yield items

class DeccanHeraldPoliticsSpider(scrapy.Spider):
	name = "dhpolitics"
	start_urls = [
		'https://www.deccanherald.com/india/politics'
	]

	def parse(self, response):
		articles = response.xpath("//div[@class='story-card']")
		for article in articles[:12]:  # Limit to 12 articles
			items = PoliticscrawlerItem()
			title = article.xpath(".//h3/a/text()").get()
			link = article.xpath(".//h3/a/@href").get()
			img = article.xpath(".//img/@src").get()
			
			if title and link:
				if not link.startswith('http'):
					link = 'https://www.deccanherald.com' + link
				
				items['title'] = title.strip()
				items['image'] = img if img else ''
				items['url'] = link
				items['source'] = 'Deccan Herald'
				yield items