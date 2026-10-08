import scrapy
from ..items import SportscrawlerItem


class SportsSpider(scrapy.Spider):
    name = "sports"
    start_urls = [
        'https://indianexpress.com/section/sports/'
    ]

    def parse(self, response):
        # Updated selector for current Indian Express structure
        articles = response.xpath("//div[@class='articles']//div[contains(@class, 'article')]")
        
        for article in articles:
            items = SportscrawlerItem()
            
            # Use relative XPath with .// instead of //
            title = article.xpath(".//h2[@class='title']/a/text()").get()
            link = article.xpath(".//h2[@class='title']/a/@href").get()
            
            # Priority order for lazy-loaded images
            img = article.xpath(".//img/@data-src").get() or \
                  article.xpath(".//img/@data-original").get() or \
                  article.xpath(".//img/@data-lazy-src").get() or \
                  article.xpath(".//noscript/img/@src").get() or \
                  article.xpath(".//img/@src").get()
            
            # Skip if image is a logo/placeholder
            if img and ('logo' in img.lower() or 'placeholder' in img.lower()):
                img = article.xpath(".//img/@data-src").get() or \
                      article.xpath(".//img/@data-original").get()
            
            # Only yield if we have required data
            if title and link:
                items["title"] = title.strip()
                items["image"] = img if img else ""
                items["url"] = link
                items['source'] = 'Indian Express'
                yield items


class HtimesSpider(scrapy.Spider):
    name = "Htimes"
    start_urls = [
        'https://www.hindustantimes.com/other-sports/'
    ]

    def parse(self, response):
        # Updated selector for current Hindustan Times structure
        articles = response.xpath("//div[contains(@class, 'cartHolder') or contains(@class, 'listView')]")
        
        for article in articles:
            items = SportscrawlerItem()
            
            # Use relative XPath with .// instead of //
            title = article.xpath(".//h3/a/text()").get() or \
                   article.xpath(".//h2/a/text()").get() or \
                   article.xpath(".//div[@class='hdg3']/a/text()").get()
            
            link = article.xpath(".//h3/a/@href").get() or \
                  article.xpath(".//h2/a/@href").get() or \
                  article.xpath(".//div[@class='hdg3']/a/@href").get()
            
            # CRITICAL: Get data-src FIRST, then data-original, then src as fallback
            # This prevents getting the logo/placeholder from src
            img = article.xpath(".//img/@data-src").get() or \
                 article.xpath(".//img/@data-original").get() or \
                 article.xpath(".//img/@data-lazy-src").get() or \
                 article.xpath(".//img/@data-lazy").get()
            
            # If still no image or if it's a logo, try backup methods
            if not img:
                src_img = article.xpath(".//img/@src").get()
                # Only use src if it's NOT a logo
                if src_img and 'logo' not in src_img.lower() and 'placeholder' not in src_img.lower():
                    img = src_img
            
            # Only yield if we have required data
            if title and link:
                # Ensure full URL
                if link.startswith('/'):
                    link = response.urljoin(link)
                    
                items["title"] = title.strip()
                items["image"] = img if img else ""
                items["url"] = link
                items['source'] = 'Hindustan Times'
                yield items
