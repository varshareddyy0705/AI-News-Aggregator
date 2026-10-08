import scrapy
from ..items import NewscrawlerItem
import xml.etree.ElementTree as ET
from datetime import datetime
import email.utils


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['techcrunch.com']
    start_urls = [
        'https://techcrunch.com/feed/'  # TechCrunch RSS feed
    ]

    def parse(self, response):
        # Parse RSS/XML feed
        root = ET.fromstring(response.body)
        
        # Find all item elements in the RSS feed
        for item in root.findall('.//item')[:20]:
            items = NewscrawlerItem()
            
            # Extract title
            title_elem = item.find('title')
            title = title_elem.text if title_elem is not None else None
            
            # Extract link
            link_elem = item.find('link')
            link = link_elem.text if link_elem is not None else None
            
            # Extract publication date
            pub_date = None
            pub_date_elem = item.find('pubDate')
            if pub_date_elem is not None and pub_date_elem.text:
                try:
                    # Parse RFC 2822 date format used in RSS
                    pub_date = datetime(*email.utils.parsedate(pub_date_elem.text)[:6])
                except:
                    pub_date = None
            
            # Extract image from media:content or enclosure
            img = None
            media_content = item.find('.//{http://search.yahoo.com/mrss/}content')
            if media_content is not None:
                img = media_content.get('url')
            else:
                enclosure = item.find('enclosure')
                if enclosure is not None:
                    img = enclosure.get('url')
            
            if title and link:
                items['title'] = title.strip()
                items['image'] = img if img else ''
                items['url'] = link
                items['source'] = 'Techcrunch'
                items['published_date'] = pub_date
                yield items


class TechSpider(scrapy.Spider):
    name = 'technews'
    allowed_domains = ['theverge.com']
    start_urls = [
        'https://www.theverge.com/rss/index.xml'  # The Verge RSS feed
    ]

    def parse(self, response):
        # Parse RSS/XML feed
        root = ET.fromstring(response.body)
        
        for item in root.findall('.//item')[:20]:
            items = NewscrawlerItem()
            
            title_elem = item.find('title')
            title = title_elem.text if title_elem is not None else None
            
            link_elem = item.find('link')
            link = link_elem.text if link_elem is not None else None
            
            # Extract publication date
            pub_date = None
            pub_date_elem = item.find('pubDate')
            if pub_date_elem is not None and pub_date_elem.text:
                try:
                    # Parse RFC 2822 date format used in RSS
                    pub_date = datetime(*email.utils.parsedate(pub_date_elem.text)[:6])
                except:
                    pub_date = None
            
            # Extract image
            img = None
            media_content = item.find('.//{http://search.yahoo.com/mrss/}content')
            if media_content is not None:
                img = media_content.get('url')
            else:
                enclosure = item.find('enclosure')
                if enclosure is not None:
                    img = enclosure.get('url')
            
            if title and link:
                items['title'] = title.strip()
                items['image'] = img if img else ''
                items['url'] = link
                items['source'] = 'The Verge'
                items['published_date'] = pub_date
                yield items


class TimesOfIndiaSpider(scrapy.Spider):
    name = 'timesofindia'
    allowed_domains = ['timesofindia.indiatimes.com']
    start_urls = [
        'https://timesofindia.indiatimes.com/rssfeeds/5880659.cms'  # TOI Tech RSS
    ]

    def parse(self, response):
        root = ET.fromstring(response.body)
        
        for item in root.findall('.//item')[:20]:
            items = NewscrawlerItem()
            
            title_elem = item.find('title')
            title = title_elem.text if title_elem is not None else None
            
            link_elem = item.find('link')
            link = link_elem.text if link_elem is not None else None
            
            # Extract publication date
            pub_date = None
            pub_date_elem = item.find('pubDate')
            if pub_date_elem is not None and pub_date_elem.text:
                try:
                    # Parse RFC 2822 date format used in RSS
                    pub_date = datetime(*email.utils.parsedate(pub_date_elem.text)[:6])
                except:
                    pub_date = None
            
            # Extract image from description or enclosure
            img = None
            enclosure = item.find('enclosure')
            if enclosure is not None:
                img = enclosure.get('url')
            
            if title and link:
                items['title'] = title.strip()
                items['image'] = img if img else ''
                items['url'] = link
                items['source'] = 'Times of India'
                items['published_date'] = pub_date
                yield items


class EconomicTimesTechSpider(scrapy.Spider):
    name = 'economictimestech'
    allowed_domains = ['economictimes.indiatimes.com']
    start_urls = [
        'https://economictimes.indiatimes.com/tech/rssfeeds/13357270.cms'  # ET Tech RSS
    ]

    def parse(self, response):
        root = ET.fromstring(response.body)
        
        for item in root.findall('.//item')[:20]:
            items = NewscrawlerItem()
            
            title_elem = item.find('title')
            title = title_elem.text if title_elem is not None else None
            
            link_elem = item.find('link')
            link = link_elem.text if link_elem is not None else None
            
            # Extract publication date
            pub_date = None
            pub_date_elem = item.find('pubDate')
            if pub_date_elem is not None and pub_date_elem.text:
                try:
                    # Parse RFC 2822 date format used in RSS
                    pub_date = datetime(*email.utils.parsedate(pub_date_elem.text)[:6])
                except:
                    pub_date = None
            
            # Extract image
            img = None
            enclosure = item.find('enclosure')
            if enclosure is not None:
                img = enclosure.get('url')
            
            if title and link:
                items['title'] = title.strip()
                items['image'] = img if img else ''
                items['url'] = link
                items['source'] = 'Economic Times Tech'
                items['published_date'] = pub_date
                yield items
