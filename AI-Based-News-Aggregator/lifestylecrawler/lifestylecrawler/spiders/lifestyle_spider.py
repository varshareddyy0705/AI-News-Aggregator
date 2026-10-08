import scrapy
from ..items import LifestylecrawlerItem
from news.models import LHeadline
from lifestylecrawler.spiders import lifestyle_spider
from lifestylecrawler import pipelines

class LifestyleSpider(scrapy.Spider):
	name = "lifestyle"
	start_urls = [
		'https://indianexpress.com/section/lifestyle/'
	]

	def parse(self, response):
		


		#div_all_news = response.xpath("//div[@class='css-13mho3u']/ol/li/div/div")
	
		for i in range(18):
			items = LifestylecrawlerItem()
			title = response.xpath("//div[@class='nation']/div[@class='articles']/h2/a/text()")[i].extract()
			link =  response.xpath("//div[@class='nation']/div[@class='articles']/div[@class='snaps']/a/@href")[i].extract()
			s = response.xpath("//div[@class='nation']/div[@class='articles']/div[@class='snaps']/a/noscript")[i].extract()
			l = s.split('"')
			img = l[5]
			l=[]
			items["title"] = title
			items["image"] = img
			items["url"] = link
			items['source'] = 'Indian Express'
			yield items

class HealthSpider(scrapy.Spider):
	name = "health"
	start_urls = [
		'https://www.foxnews.com/health'
	]

	def parse(self, response):
		


		#div_all_news = response.xpath("//div[@class='css-13mho3u']/ol/li/div/div")
	
		for i in range(12):
			items = LifestylecrawlerItem()
			title = response.xpath("//div[@class='content article-list']/article/div[@class='info']/header/h4/a/text()")[i].extract()
			link = 'https://www.foxnews.com' + response.xpath("//div[@class='content article-list']/article/div[@class='m']/a/@href")[i].extract()
			img = img = response.xpath("//div[@class='content article-list']/article/div[@class='m']/a/img/@src")[i].extract()
			items["title"] = title
			items["image"] = img
			items["url"] = link
			items['source'] = 'Fox News'
			yield items

class TimesOfIndiaLifestyleSpider(scrapy.Spider):
	name = "toilifestyle"
	start_urls = [
		'https://timesofindia.indiatimes.com/life-style'
	]

	def parse(self, response):
		articles = response.xpath("//div[@class='uwU81']")
		for article in articles[:12]:  # Limit to 12 articles
			items = LifestylecrawlerItem()
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

class DeccanHeraldLifestyleSpider(scrapy.Spider):
	name = "dhlifestyle"
	start_urls = [
		'https://www.deccanherald.com/lifestyle'
	]

	def parse(self, response):
		articles = response.xpath("//div[@class='story-card']")
		for article in articles[:12]:  # Limit to 12 articles
			items = LifestylecrawlerItem()
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
			