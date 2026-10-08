import scrapy
from ..items import EntertainmentcrawlerItem


class EntertainmentSpider(scrapy.Spider):
    name = "entertainment"
    allowed_domains = ['variety.com']
    start_urls = [
        'https://variety.com/'
    ]

    def parse(self, response):
        # Variety.com uses multiple article layouts
        articles = response.xpath(
            "//article[contains(@class, 'o-tease')] | "
            "//div[@class='l-river__content']//article | "
            "//div[contains(@class, 'c-card')]"
        )
        
        for article in articles[:15]:  # Get first 15 articles
            items = EntertainmentcrawlerItem()
            
            # Multiple title selectors for different layouts
            title = article.xpath(".//h3//a/text()").get() or \
                   article.xpath(".//h2//a/text()").get() or \
                   article.xpath(".//header//h3/a/text()").get() or \
                   article.xpath(".//a[@class='c-title__link']/text()").get()
            
            # Multiple link selectors
            link = article.xpath(".//h3//a/@href").get() or \
                  article.xpath(".//h2//a/@href").get() or \
                  article.xpath(".//header//h3/a/@href").get() or \
                  article.xpath(".//a[@class='c-title__link']/@href").get() or \
                  article.xpath(".//figure//a/@href").get()
            
            # Priority for lazy-loaded images - Variety specific
            img = article.xpath(".//img/@data-src").get() or \
                 article.xpath(".//img/@data-lazy-src").get() or \
                 article.xpath(".//img/@data-original").get() or \
                 article.xpath(".//source/@data-srcset").get()
            
            # Fallback to src but filter logos/sprites
            if not img:
                src_img = article.xpath(".//img/@src").get()
                if src_img and not any(x in src_img.lower() for x in ['logo', 'sprite', 'blank', 'placeholder']):
                    img = src_img
            
            # Clean srcset values (extract first URL)
            if img and ' ' in img:
                img = img.split(' ')[0].split(',')[0]
            
            # Ensure full URL
            if link and not link.startswith('http'):
                link = response.urljoin(link)
            
            if title and link:
                items["title"] = title.strip()
                items["image"] = img if img else ''
                items["url"] = link
                items['source'] = 'Variety'
                yield items


class EntrtnmentSpider(scrapy.Spider):
    name = "entrtnment"
    allowed_domains = ['indianexpress.com']
    start_urls = [
        'https://indianexpress.com/section/entertainment/'
    ]

    def parse(self, response):
        # Indian Express Entertainment section
        articles = response.xpath(
            "//div[@class='articles']//article | "
            "//div[@class='nation']//div[@class='articles'] | "
            "//div[contains(@class, 'article')]"
        )
        
        for article in articles[:20]:  # Get first 20 articles
            items = EntertainmentcrawlerItem()
            
            # Multiple title selectors
            title = article.xpath(".//h2/a/text()").get() or \
                   article.xpath(".//h3/a/text()").get() or \
                   article.xpath(".//div[@class='title']/a/text()").get()
            
            # Multiple link selectors
            link = article.xpath(".//h2/a/@href").get() or \
                  article.xpath(".//h3/a/@href").get() or \
                  article.xpath(".//div[@class='title']/a/@href").get() or \
                  article.xpath(".//div[@class='snaps']/a/@href").get()
            
            # Priority for lazy-loaded images - Indian Express specific
            img = article.xpath(".//img/@data-lazy-src").get() or \
                 article.xpath(".//img/@data-src").get() or \
                 article.xpath(".//img/@data-original").get() or \
                 article.xpath(".//noscript/img/@src").get()
            
            # Fallback to src but filter logos
            if not img:
                src_img = article.xpath(".//img/@src").get()
                if src_img and not any(x in src_img.lower() for x in ['logo', 'sprite', 'blank', 'placeholder']):
                    img = src_img
            
            # Clean srcset values
            if img and ' ' in img:
                img = img.split(' ')[0].split(',')[0]
            
            if title and link:
                items["title"] = title.strip()
                items["image"] = img if img else ''
                items["url"] = link
                items['source'] = 'Indian Express'
                yield items
