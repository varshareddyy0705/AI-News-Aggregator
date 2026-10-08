import scrapy
from ..items import EconomycrawlerItem


class EconomySpider(scrapy.Spider):
    name = "economy"
    allowed_domains = ['economictimes.indiatimes.com']
    start_urls = [
        'https://economictimes.indiatimes.com/markets/stocks/news'
    ]

    def parse(self, response):
        # Economic Times uses multiple article containers
        articles = response.xpath("//div[contains(@class, 'eachStory') or contains(@class, 'story')]")
        
        for article in articles[:15]:  # Get more articles
            items = EconomycrawlerItem()
            
            # Multiple title selectors for different layouts
            title = article.xpath(".//h3/a/text()").get() or \
                   article.xpath(".//h2/a/text()").get() or \
                   article.xpath(".//h4/a/text()").get() or \
                   article.xpath(".//a[@class='storylink']/text()").get()
            
            link = article.xpath(".//h3/a/@href").get() or \
                  article.xpath(".//h2/a/@href").get() or \
                  article.xpath(".//h4/a/@href").get() or \
                  article.xpath(".//a[@class='storylink']/@href").get()
            
            # Priority: data-original > data-src > src
            img = article.xpath(".//img/@data-original").get() or \
                 article.xpath(".//img/@data-src").get() or \
                 article.xpath(".//img/@data-lazy").get() or \
                 article.xpath(".//picture/source/@data-srcset").get()
            
            # Fallback to src only if not a logo
            if not img:
                src_img = article.xpath(".//img/@src").get()
                if src_img and 'logo' not in src_img.lower() and 'sprite' not in src_img.lower():
                    img = src_img
            
            # Extract first URL from srcset if needed
            if img and ' ' in img:
                img = img.split(' ')[0]
            
            if title and link:
                # Ensure full URL
                if not link.startswith('http'):
                    link = "https://economictimes.indiatimes.com" + link
                
                items["title"] = title.strip()
                items["image"] = img if img else ''
                items["url"] = link
                items['source'] = 'Economic Times'
                yield items


class ExpressSpider(scrapy.Spider):
    name = "express"
    allowed_domains = ['indianexpress.com']
    start_urls = [
        'https://indianexpress.com/section/business/economy/'
    ]

    def parse(self, response):
        # Indian Express uses article containers with various classes
        articles = response.xpath("//div[@class='articles']//article | //div[contains(@class, 'article')]")
        
        for article in articles[:15]:  # Get more articles
            items = EconomycrawlerItem()
            
            title = article.xpath(".//h2/a/text()").get() or \
                   article.xpath(".//h3/a/text()").get()
            
            link = article.xpath(".//h2/a/@href").get() or \
                  article.xpath(".//h3/a/@href").get()
            
            # Priority for lazy-loaded images
            img = article.xpath(".//img/@data-lazy-src").get() or \
                 article.xpath(".//img/@data-src").get() or \
                 article.xpath(".//img/@data-original").get() or \
                 article.xpath(".//source/@data-srcset").get()
            
            # Fallback to src but avoid logos
            if not img:
                src_img = article.xpath(".//img/@src").get()
                if src_img and 'logo' not in src_img.lower() and 'sprite' not in src_img.lower():
                    img = src_img
            
            # Clean srcset values
            if img and ' ' in img:
                img = img.split(' ')[0]
            
            if title and link:
                items["title"] = title.strip()
                items["image"] = img if img else ''
                items["url"] = link
                items['source'] = 'Indian Express'
                yield items


class MoneyControlSpider(scrapy.Spider):
    name = "moneycontrol"
    allowed_domains = ['moneycontrol.com']
    start_urls = [
        'https://www.moneycontrol.com/news/business/economy/'
    ]

    def parse(self, response):
        # MoneyControl uses list items with clearfix class
        articles = response.xpath("//li[@class='clearfix'] | //li[contains(@class, 'newslist')] | //ul[contains(@class, 'listing')]/li")
        
        for article in articles[:15]:  # Get more articles
            items = EconomycrawlerItem()
            
            # Multiple title selectors
            title = article.xpath(".//h2/a/text()").get() or \
                   article.xpath(".//h3/a/text()").get() or \
                   article.xpath(".//p[@class='title']/a/text()").get()
            
            link = article.xpath(".//h2/a/@href").get() or \
                  article.xpath(".//h3/a/@href").get() or \
                  article.xpath(".//p[@class='title']/a/@href").get()
            
            # Priority for lazy-loaded images - MoneyControl specific
            img = article.xpath(".//img/@data-src").get() or \
                 article.xpath(".//img/@data-lazy").get() or \
                 article.xpath(".//img/@data-original").get()
            
            # Fallback to src but filter out logos and placeholders
            if not img:
                src_img = article.xpath(".//img/@src").get()
                if src_img and not any(x in src_img.lower() for x in ['logo', 'sprite', 'placeholder', 'blank']):
                    img = src_img
            
            # Clean srcset values
            if img and ' ' in img:
                img = img.split(' ')[0]
            
            if title and link:
                items["title"] = title.strip()
                items["image"] = img if img else ''
                items["url"] = link
                items['source'] = 'MoneyControl'
                yield items
