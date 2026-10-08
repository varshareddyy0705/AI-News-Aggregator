from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import feedparser
from dateutil import parser as date_parser
from news.models import Headline, EHeadline, SHeadline, PHeadline, LHeadline, ENHeadline


class Command(BaseCommand):
    help = 'Fetch real Indian news from RSS feeds'

    def fetch_rss_feed(self, feed_url):
        """Parse RSS feed and return entries"""
        try:
            feed = feedparser.parse(feed_url)
            return feed.entries
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to parse {feed_url}: {str(e)}'))
            return []

    def handle(self, *args, **options):
        # Clear existing data
        self.stdout.write('Clearing existing news...')
        Headline.objects.all().delete()
        EHeadline.objects.all().delete()
        SHeadline.objects.all().delete()
        PHeadline.objects.all().delete()
        LHeadline.objects.all().delete()
        ENHeadline.objects.all().delete()
        
        # Define cutoff date (10 days ago)
        cutoff_date = timezone.now() - timedelta(days=10)
        total_created = 0
        
        # RSS Feed sources: (feed_url, model, category_name)
        rss_sources = [
            # Technology
            ('https://timesofindia.indiatimes.com/rssfeeds/66949542.cms', Headline, 'Technology'),
            ('https://www.thehindu.com/sci-tech/technology/feeder/default.rss', Headline, 'Technology'),
            
            # Business/Economy
            ('https://timesofindia.indiatimes.com/rssfeeds/1898055.cms', EHeadline, 'Business'),
            ('https://www.thehindu.com/business/feeder/default.rss', EHeadline, 'Business'),
            
            # Sports
            ('https://timesofindia.indiatimes.com/rssfeeds/4719148.cms', SHeadline, 'Sports'),
            ('https://www.thehindu.com/sport/feeder/default.rss', SHeadline, 'Sports'),
            
            # Politics/General
            ('https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms', PHeadline, 'India News'),
            ('https://www.thehindu.com/news/national/feeder/default.rss', PHeadline, 'National'),
            
            # Lifestyle
            ('https://timesofindia.indiatimes.com/rssfeeds/3908999.cms', LHeadline, 'Lifestyle'),
            ('https://www.thehindu.com/life-and-style/feeder/default.rss', LHeadline, 'Life & Style'),
            
            # Entertainment
            ('https://timesofindia.indiatimes.com/rssfeeds/1081479906.cms', ENHeadline, 'Entertainment'),
            ('https://indianexpress.com/section/entertainment/rss/', ENHeadline, 'Entertainment'),
        ]
        
        for feed_url, model, category_name in rss_sources:
            self.stdout.write(f'\nFetching {category_name} news from RSS...')
            
            entries = self.fetch_rss_feed(feed_url)
            count = 0
            
            for entry in entries:
                # Parse published date
                published_date = timezone.now()
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    import time
                    published_date = timezone.make_aware(
                        timezone.datetime.fromtimestamp(time.mktime(entry.published_parsed))
                    )
                elif hasattr(entry, 'published'):
                    try:
                        published_date = date_parser.parse(entry.published)
                        if timezone.is_naive(published_date):
                            published_date = timezone.make_aware(published_date)
                    except:
                        pass
                
                # Only include news from the past 10 days
                if published_date < cutoff_date:
                    continue
                
                # Extract image
                image_url = 'https://via.placeholder.com/800x600'
                if hasattr(entry, 'media_content') and entry.media_content:
                    image_url = entry.media_content[0].get('url', image_url)
                elif hasattr(entry, 'enclosures') and entry.enclosures:
                    image_url = entry.enclosures[0].get('href', image_url)
                
                # Create news entry
                model.objects.create(
                    title=entry.get('title', 'No title')[:500],
                    image=image_url,
                    url=entry.get('link', ''),
                    source=category_name,
                    published_date=published_date,
                    created_at=published_date,
                    is_live=True
                )
                count += 1
                total_created += 1
            
            self.stdout.write(self.style.SUCCESS(f'✓ Created {count} {category_name} articles'))
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Successfully created {total_created} real news articles!'))
