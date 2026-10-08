import requests
import time
from django.shortcuts import render, redirect
from uuid import uuid4
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
from news.models import Headline,EHeadline,SHeadline,PHeadline,LHeadline,ENHeadline
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.conf import settings as django_settings
from django.utils import timezone
from datetime import timedelta
from itertools import chain
from django.core.paginator import Paginator

#for scrapy
import os
import sys

path = django_settings.BASE_DIR
sys.path.append(path + "/newscrawler")
sys.path.append(path + "/economycrawler")
sys.path.append(path + "/sportscrawler")
sys.path.append(path + "/politicscrawler")
sys.path.append(path + "/lifestylecrawler")
sys.path.append(path + "/entertainmentcrawler")


# sys.path.append("C:/Users/admin/Desktop/DJANGO/Practice_Django/News_Aggregator/newscrawler")
# sys.path.append("C:/Users/admin/Desktop/DJANGO/Practice_Django/News_Aggregator/economycrawler")
# sys.path.append("C:/Users/admin/Desktop/DJANGO/Practice_Django/News_Aggregator/sportscrawler")
# sys.path.append("C:/Users/admin/Desktop/DJANGO/Practice_Django/News_Aggregator/politicscrawler")
# sys.path.append("C:/Users/admin/Desktop/DJANGO/Practice_Django/News_Aggregator/lifestylecrawler")
# sys.path.append("C:/Users/admin/Desktop/DJANGO/Practice_Django/News_Aggregator/entertainmentcrawler")

from newscrawler.spiders import news_spider
from economycrawler.spiders import economy_spider
from sportscrawler.spiders import sports_spider
from politicscrawler.spiders import politics_spider
from lifestylecrawler.spiders import lifestyle_spider
from entertainmentcrawler.spiders import entertainment_spider
from newscrawler.pipelines import NewscrawlerPipeline
from scrapy import signals
from twisted.internet import reactor
from scrapy.crawler import Crawler,CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from newscrawler import settings as my_settings
from economycrawler import settings as economy_settings
from sportscrawler import settings as sports_settings
from politicscrawler import settings as politics_settings
from lifestylecrawler import settings as lifestyle_settings
from entertainmentcrawler import settings as entertainment_settings 
from scrapy.utils.log import configure_logging
from crochet import setup



#scrapyd = ScrapydAPI('http://localhost:6800')

def home1(request):
    return render(request, "news/starter.html")
'''
@login_required
def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context ={
            'object_list' : headlines,
    }
    return render(request, "news/home.html", context)
'''

class NewsListView(ListView):
    model = Headline
    template_name = 'news/home.html'
    paginate_by = 5
'''
@login_required
def economy_news_list(request):
    headlines = EHeadline.objects.all()[::-1]
    context ={
            'object_list' : headlines,
    }
    return render(request, "news/economy_home.html", context)
'''

class EconomyListView(ListView):
    model = EHeadline
    template_name = 'news/economy_home.html'
    paginate_by = 5
'''
@login_required
def sports_news_list(request):
    headlines = SHeadline.objects.all()[::-1]
    context ={
            'object_list' : headlines,
    }
    return render(request, "news/sports_home.html", context)
'''
class SportsListView(ListView):
    model = SHeadline
    template_name = 'news/sports_home.html'
    paginate_by = 5


class PoliticsListView(ListView):
    model = PHeadline
    template_name = 'news/politics_home.html'
    paginate_by = 5

class LifestyleListView(ListView):
    model = LHeadline
    template_name = 'news/lifestyle_home.html'
    paginate_by = 5

class EntertainmentListView(ListView):
    model = ENHeadline
    template_name = 'news/entertainment_home.html'
    paginate_by = 5


@login_required
def menu_list(request):
    return render(request, "news/topics_list.html")


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def scrape(request):
    # Headline.objects.all().delete()
    crawler_settings = Settings()

    setup()
    configure_logging()
    crawler_settings.setmodule(my_settings)
    runner= CrawlerRunner(settings=crawler_settings)
    # Use working tech spiders
    d=runner.crawl(news_spider.NewsSpider)
    time.sleep(3)
    d=runner.crawl(news_spider.TechSpider)
    time.sleep(3)
    d=runner.crawl(news_spider.TimesOfIndiaSpider)
    time.sleep(3)
    d=runner.crawl(news_spider.EconomicTimesTechSpider)
    time.sleep(3)
    return redirect("../getnews/")

@csrf_exempt
@require_http_methods(['POST', 'GET'])
def scrape1(request):
    # EHeadline.objects.all().delete()
    crawler_settings = Settings()

    setup()
    configure_logging()
    crawler_settings.setmodule(economy_settings)
    runner= CrawlerRunner(settings=crawler_settings)
    d=runner.crawl(economy_spider.EconomySpider)
    time.sleep(3)
    d=runner.crawl(economy_spider.ExpressSpider)
    time.sleep(3)
    return redirect("../geteconomynews/")


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def scrape2(request):
    # SHeadline.objects.all().delete()
    crawler_settings = Settings()

    setup()
    configure_logging()
    crawler_settings.setmodule(sports_settings)
    runner= CrawlerRunner(settings=crawler_settings)
    d=runner.crawl(sports_spider.SportsSpider)
    time.sleep(3)
    d=runner.crawl(sports_spider.HtimesSpider)
    time.sleep(3)
    return redirect("../getsportsnews/")


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def scrape3(request):
    # PHeadline.objects.all().delete()
    crawler_settings = Settings()

    setup()
    configure_logging()
    crawler_settings.setmodule(politics_settings)
    runner= CrawlerRunner(settings=crawler_settings)
    # Only use working spiders - removed PoliticsSpider (NYTimes blocked) and DeccanHeraldPoliticsSpider (403 error)
    d=runner.crawl(politics_spider.EconomicSpider)
    time.sleep(3)
    d=runner.crawl(politics_spider.TimesOfIndiaPoliticsSpider)
    time.sleep(3)
    return redirect("../getpoliticsnews/")


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def scrape4(request):
    # LHeadline.objects.all().delete()
    crawler_settings = Settings()

    setup()
    configure_logging()
    crawler_settings.setmodule(lifestyle_settings)
    runner= CrawlerRunner(settings=crawler_settings)
    d=runner.crawl(lifestyle_spider.LifestyleSpider)
    time.sleep(3)
    d=runner.crawl(lifestyle_spider.HealthSpider)
    time.sleep(3)
    d=runner.crawl(lifestyle_spider.TimesOfIndiaLifestyleSpider)
    time.sleep(3)
    d=runner.crawl(lifestyle_spider.DeccanHeraldLifestyleSpider)
    time.sleep(3)
    return redirect("../getlifestylenews/")


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def scrape5(request):
    # ENHeadline.objects.all().delete()
    crawler_settings = Settings()

    setup()
    configure_logging()
    crawler_settings.setmodule(entertainment_settings)
    runner= CrawlerRunner(settings=crawler_settings)
    d=runner.crawl(entertainment_spider.EntertainmentSpider)
    time.sleep(3)
    d=runner.crawl(entertainment_spider.EntrtnmentSpider)
    time.sleep(3)
    return redirect("../getentertainmentnews/")


# New view for all news categories combined
def all_news_view(request):
    # Get all news from different categories
    tech_news = list(Headline.objects.all())
    economy_news = list(EHeadline.objects.all())
    sports_news = list(SHeadline.objects.all())
    # politics_news = list(PHeadline.objects.all())
    # lifestyle_news = list(LHeadline.objects.all())
    entertainment_news = list(ENHeadline.objects.all())
    
    # Add category field to each news item
    for item in tech_news:
        item.category = 'Technology'
    for item in economy_news:
        item.category = 'Economy'
    for item in sports_news:
        item.category = 'Sports'
    # for item in politics_news:
    #     item.category = 'Politics'
    # for item in lifestyle_news:
    #     item.category = 'Lifestyle'
    for item in entertainment_news:
        item.category = 'Entertainment'
    
    # Combine all news and sort by created_at
    all_news = tech_news + economy_news + sports_news  + entertainment_news
    all_news.sort(key=lambda x: x.created_at, reverse=True)
    
    # Pagination
    paginator = Paginator(all_news, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'object_list': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator,
    }
    return render(request, 'news/all_news.html', context)


# New view for live/latest news
def live_news_view(request):
    # Get news from last 24 hours
    last_24_hours = timezone.now() - timedelta(hours=24)
    
    # Get recent news from all categories
    tech_news = list(Headline.objects.filter(created_at__gte=last_24_hours))
    economy_news = list(EHeadline.objects.filter(created_at__gte=last_24_hours))
    sports_news = list(SHeadline.objects.filter(created_at__gte=last_24_hours))
    politics_news = list(PHeadline.objects.filter(created_at__gte=last_24_hours))
    lifestyle_news = list(LHeadline.objects.filter(created_at__gte=last_24_hours))
    entertainment_news = list(ENHeadline.objects.filter(created_at__gte=last_24_hours))
    
    # Add category field to each news item
    for item in tech_news:
        item.category = 'Technology'
        item.is_live = True
    for item in economy_news:
        item.category = 'Economy'
        item.is_live = True
    for item in sports_news:
        item.category = 'Sports'
        item.is_live = True
    for item in politics_news:
        item.category = 'Politics'
        item.is_live = True
    for item in lifestyle_news:
        item.category = 'Lifestyle'
        item.is_live = True
    for item in entertainment_news:
        item.category = 'Entertainment'
        item.is_live = True
    
    # Combine all live news and sort by created_at
    live_news = tech_news + economy_news + sports_news + politics_news + lifestyle_news + entertainment_news
    live_news.sort(key=lambda x: x.created_at, reverse=True)
    
    # Pagination
    paginator = Paginator(live_news, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'object_list': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator,
        'is_live_view': True,
    }
    return render(request, 'news/live_news.html', context)


# Scrape all categories at once
@csrf_exempt
@require_http_methods(['POST', 'GET'])
def scrape_all(request):
    # Clear all existing data
    # Headline.objects.all().delete()
    # EHeadline.objects.all().delete()
    # SHeadline.objects.all().delete()
    # PHeadline.objects.all().delete()
    # LHeadline.objects.all().delete()
    # ENHeadline.objects.all().delete()
    
    crawler_settings = Settings()
    setup()
    configure_logging()

    scrape(request)

    scrape1(request)

    scrape2(request)

    scrape3(request)

    scrape4(request)

    scrape5(request)
    
    # Scrape Technology news
    # crawler_settings.setmodule(my_settings)
    # runner = CrawlerRunner(settings=crawler_settings)
    # d = runner.crawl(news_spider.TimesOfIndiaSpider)
    # time.sleep(3)
    # d = runner.crawl(news_spider.DeccanHeraldSpider)
    # time.sleep(3)
    
    # # Scrape Economy news
    # crawler_settings.setmodule(economy_settings)
    # runner = CrawlerRunner(settings=crawler_settings)
    # d = runner.crawl(economy_spider.EconomySpider)
    # time.sleep(3)
    # d = runner.crawl(economy_spider.ExpressSpider)
    # time.sleep(3)
    
    # # Scrape Sports news
    # crawler_settings.setmodule(sports_settings)
    # runner = CrawlerRunner(settings=crawler_settings)
    # d = runner.crawl(sports_spider.SportsSpider)
    # time.sleep(3)
    # d = runner.crawl(sports_spider.HtimesSpider)
    # time.sleep(3)
    
    # # Scrape Politics news
    # crawler_settings.setmodule(politics_settings)
    # runner = CrawlerRunner(settings=crawler_settings)
    # d = runner.crawl(politics_spider.TimesOfIndiaPoliticsSpider)
    # time.sleep(3)
    # d = runner.crawl(politics_spider.DeccanHeraldPoliticsSpider)
    # time.sleep(3)
    
    # # Scrape Lifestyle news
    # crawler_settings.setmodule(lifestyle_settings)
    # runner = CrawlerRunner(settings=crawler_settings)
    # d = runner.crawl(lifestyle_spider.TimesOfIndiaLifestyleSpider)
    # time.sleep(3)
    # d = runner.crawl(lifestyle_spider.DeccanHeraldLifestyleSpider)
    # time.sleep(3)
    
    # # Scrape Entertainment news
    # crawler_settings.setmodule(entertainment_settings)
    # runner = CrawlerRunner(settings=crawler_settings)
    # d = runner.crawl(entertainment_spider.EntertainmentSpider)
    # time.sleep(3)
    # d = runner.crawl(entertainment_spider.EntrtnmentSpider)
    # time.sleep(3)
    
    return redirect("../all-news/")

# from django.shortcuts import render
# from django.core.paginator import Paginator
# from django.utils import timezone
# from datetime import timedelta
# from django.db.models import Q
# from .models import Headline, EHeadline, SHeadline, PHeadline, LHeadline, ENHeadline

# def ten_day_news_view(request):
#     # Get date filter parameters
#     days = int(request.GET.get('days', 10))  # Default 10 days
#     specific_date = request.GET.get('date', None)  # For specific date filter
    
#     if specific_date:
#         # If specific date is provided, show news from that date only
#         from datetime import datetime
#         filter_date = datetime.strptime(specific_date, '%Y-%m-%d').date()
#         # Show news from that entire day
#         start_date = timezone.make_aware(datetime.combine(filter_date, datetime.min.time()))
#         end_date = timezone.make_aware(datetime.combine(filter_date, datetime.max.time()))
        
#         # Filter by published_date if available, otherwise by created_at
#         tech_news = list(Headline.objects.filter(
#             Q(published_date__range=(start_date, end_date)) | 
#             Q(published_date__isnull=True, created_at__range=(start_date, end_date))
#         ))
#         economy_news = list(EHeadline.objects.filter(
#             Q(published_date__range=(start_date, end_date)) | 
#             Q(published_date__isnull=True, created_at__range=(start_date, end_date))
#         ))
#         sports_news = list(SHeadline.objects.filter(
#             Q(published_date__range=(start_date, end_date)) | 
#             Q(published_date__isnull=True, created_at__range=(start_date, end_date))
#         ))
#         politics_news = list(PHeadline.objects.filter(
#             Q(published_date__range=(start_date, end_date)) | 
#             Q(published_date__isnull=True, created_at__range=(start_date, end_date))
#         ))
#         lifestyle_news = list(LHeadline.objects.filter(
#             Q(published_date__range=(start_date, end_date)) | 
#             Q(published_date__isnull=True, created_at__range=(start_date, end_date))
#         ))
#         entertainment_news = list(ENHeadline.objects.filter(
#             Q(published_date__range=(start_date, end_date)) | 
#             Q(published_date__isnull=True, created_at__range=(start_date, end_date))
#         ))
#     else:
#         # Get news from last X days
#         last_days = timezone.now() - timedelta(days=days)
        
#         # Filter by published_date if available, otherwise by created_at
#         tech_news = list(Headline.objects.filter(
#             Q(published_date__gte=last_days) | 
#             Q(published_date__isnull=True, created_at__gte=last_days)
#         ))
#         economy_news = list(EHeadline.objects.filter(
#             Q(published_date__gte=last_days) | 
#             Q(published_date__isnull=True, created_at__gte=last_days)
#         ))
#         sports_news = list(SHeadline.objects.filter(
#             Q(published_date__gte=last_days) | 
#             Q(published_date__isnull=True, created_at__gte=last_days)
#         ))
#         politics_news = list(PHeadline.objects.filter(
#             Q(published_date__gte=last_days) | 
#             Q(published_date__isnull=True, created_at__gte=last_days)
#         ))
#         lifestyle_news = list(LHeadline.objects.filter(
#             Q(published_date__gte=last_days) | 
#             Q(published_date__isnull=True, created_at__gte=last_days)
#         ))
#         entertainment_news = list(ENHeadline.objects.filter(
#             Q(published_date__gte=last_days) | 
#             Q(published_date__isnull=True, created_at__gte=last_days)
#         ))
    
#     # Add category field to each news item
#     for item in tech_news:
#         item.category = 'Technology'
#     for item in economy_news:
#         item.category = 'Economy'
#     for item in sports_news:
#         item.category = 'Sports'
#     for item in politics_news:
#         item.category = 'Politics'
#     for item in lifestyle_news:
#         item.category = 'Lifestyle'
#     for item in entertainment_news:
#         item.category = 'Entertainment'
    
#     # Combine all news
#     ten_day_news = tech_news + economy_news + sports_news + politics_news + lifestyle_news + entertainment_news
    
#     # Sort by published_date if available, otherwise by created_at
#     ten_day_news.sort(key=lambda x: x.published_date if x.published_date else x.created_at, reverse=True)
    
#     # Pagination
#     paginator = Paginator(ten_day_news, 15)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     context = {
#         'object_list': page_obj,
#         'page_obj': page_obj,
#         'is_paginated': page_obj.has_other_pages(),
#         'paginator': paginator,
#         'is_ten_day_view': True,
#         'total_news_count': len(ten_day_news),
#         'current_days': days,
#         'specific_date': specific_date,
#     }
#     return render(request, 'news/ten_day_news.html', context)


# from django.shortcuts import render
# from django.core.paginator import Paginator
# from django.utils import timezone
# from datetime import timedelta, datetime
# from django.db.models import Q
# from .models import Headline, EHeadline, SHeadline, PHeadline, LHeadline, ENHeadline

# def ten_day_news_view(request):
#     # Get filter parameters
#     days = int(request.GET.get('days', 10))  # Default 10 days
#     specific_date = request.GET.get('date', None)  # For specific date filter
#     category = request.GET.get('category', 'all')  # Category filter
    
#     # Define date range
#     if specific_date:
#         # If specific date is provided, show news from that date only
#         filter_date = datetime.strptime(specific_date, '%Y-%m-%d').date()
#         start_date = timezone.make_aware(datetime.combine(filter_date, datetime.min.time()))
#         end_date = timezone.make_aware(datetime.combine(filter_date, datetime.max.time()))
#     else:
#         # Get news from last X days
#         start_date = timezone.now() - timedelta(days=days)
#         end_date = timezone.now()
    
#     # Initialize empty lists
#     tech_news = []
#     economy_news = []
#     sports_news = []
#     politics_news = []
#     lifestyle_news = []
#     entertainment_news = []
    
#     # Fetch news based on category selection
#     if category == 'all' or category == 'technology':
#         tech_news = list(Headline.objects.filter(
#             Q(published_date__gte=start_date, published_date__lte=end_date) | 
#             Q(published_date__isnull=True, created_at__gte=start_date, created_at__lte=end_date)
#         ))
#         for item in tech_news:
#             item.category = 'Technology'
    
#     if category == 'all' or category == 'economy':
#         economy_news = list(EHeadline.objects.filter(
#             Q(published_date__gte=start_date, published_date__lte=end_date) | 
#             Q(published_date__isnull=True, created_at__gte=start_date, created_at__lte=end_date)
#         ))
#         for item in economy_news:
#             item.category = 'Economy'
    
#     if category == 'all' or category == 'sports':
#         sports_news = list(SHeadline.objects.filter(
#             Q(published_date__gte=start_date, published_date__lte=end_date) | 
#             Q(published_date__isnull=True, created_at__gte=start_date, created_at__lte=end_date)
#         ))
#         for item in sports_news:
#             item.category = 'Sports'
    
#     if category == 'all' or category == 'politics':
#         politics_news = list(PHeadline.objects.filter(
#             Q(published_date__gte=start_date, published_date__lte=end_date) | 
#             Q(published_date__isnull=True, created_at__gte=start_date, created_at__lte=end_date)
#         ))
#         for item in politics_news:
#             item.category = 'Politics'
    
#     if category == 'all' or category == 'lifestyle':
#         lifestyle_news = list(LHeadline.objects.filter(
#             Q(published_date__gte=start_date, published_date__lte=end_date) | 
#             Q(published_date__isnull=True, created_at__gte=start_date, created_at__lte=end_date)
#         ))
#         for item in lifestyle_news:
#             item.category = 'Lifestyle'
    
#     if category == 'all' or category == 'entertainment':
#         entertainment_news = list(ENHeadline.objects.filter(
#             Q(published_date__gte=start_date, published_date__lte=end_date) | 
#             Q(published_date__isnull=True, created_at__gte=start_date, created_at__lte=end_date)
#         ))
#         for item in entertainment_news:
#             item.category = 'Entertainment'
    
#     # Combine all news
#     ten_day_news = tech_news + economy_news + sports_news + politics_news + lifestyle_news + entertainment_news
    
#     # Sort by published_date if available, otherwise by created_at
#     ten_day_news.sort(key=lambda x: x.published_date if x.published_date else x.created_at, reverse=True)
    
#     # Pagination
#     paginator = Paginator(ten_day_news, 15)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     # Category choices for dropdown
#     categories = [
#         ('all', 'All Categories'),
#         ('technology', 'Technology'),
#         ('economy', 'Economy'),
#         ('sports', 'Sports'),
#         # ('politics', 'Politics'),
#         # ('lifestyle', 'Lifestyle'),
#         ('entertainment', 'Entertainment'),
#     ]
    
#     context = {
#         'object_list': page_obj,
#         'page_obj': page_obj,
#         'is_paginated': page_obj.has_other_pages(),
#         'paginator': paginator,
#         'is_ten_day_view': True,
#         'total_news_count': len(ten_day_news),
#         'current_days': days,
#         'specific_date': specific_date,
#         'categories': categories,
#         'selected_category': category,
#     }
#     return render(request, 'news/ten_day_news.html', context)


from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Q
from .models import Headline, EHeadline, SHeadline, ENHeadline


def ten_day_news_view(request):
    # Get filter parameters
    days = int(request.GET.get('days', 5))  # Default 5 days
    specific_date = request.GET.get('date', None)  # For specific date filter
    category = request.GET.get('category', 'all')  # Category filter
    
    # Define date range
    if specific_date:
        # If specific date is provided, show news from that date only
        filter_date = datetime.strptime(specific_date, '%Y-%m-%d').date()
        start_date = timezone.make_aware(datetime.combine(filter_date, datetime.min.time()))
        end_date = timezone.make_aware(datetime.combine(filter_date, datetime.max.time()))
    else:
        # Get news from last X days
        start_date = timezone.now() - timedelta(days=days)
        end_date = timezone.now()
    
    # Initialize empty lists
    tech_news = []
    economy_news = []
    sports_news = []
    entertainment_news = []
    
    # Fetch news based on category selection
    if category == 'all' or category == 'technology':
        tech_news = list(Headline.objects.filter(
            Q(published_date__gte=start_date, published_date__lte=end_date) | 
            Q(published_date__isnull=True, created_at__gte=start_date, created_at__lte=end_date)
        ))
        for item in tech_news:
            item.category = 'Technology'
    
    if category == 'all' or category == 'economy':
        economy_news = list(EHeadline.objects.filter(
            Q(published_date__gte=start_date, published_date__lte=end_date) | 
            Q(published_date__isnull=True, created_at__gte=start_date, created_at__lte=end_date)
        ))
        for item in economy_news:
            item.category = 'Economy'
    
    if category == 'all' or category == 'sports':
        sports_news = list(SHeadline.objects.filter(
            Q(published_date__gte=start_date, published_date__lte=end_date) | 
            Q(published_date__isnull=True, created_at__gte=start_date, created_at__lte=end_date)
        ))
        for item in sports_news:
            item.category = 'Sports'
    
    if category == 'all' or category == 'entertainment':
        entertainment_news = list(ENHeadline.objects.filter(
            Q(published_date__gte=start_date, published_date__lte=end_date) | 
            Q(published_date__isnull=True, created_at__gte=start_date, created_at__lte=end_date)
        ))
        for item in entertainment_news:
            item.category = 'Entertainment'
    
    # Combine all news
    ten_day_news = tech_news + economy_news + sports_news + entertainment_news
    
    # Sort by published_date if available, otherwise by created_at
    ten_day_news.sort(key=lambda x: x.published_date if x.published_date else x.created_at, reverse=True)
    
    # Pagination
    paginator = Paginator(ten_day_news, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Category choices for dropdown
    categories = [
        ('all', 'All Categories'),
        ('technology', 'Technology'),
        ('economy', 'Economy'),
        ('sports', 'Sports'),
        ('entertainment', 'Entertainment'),
    ]
    
    context = {
        'object_list': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator,
        'is_ten_day_view': True,
        'total_news_count': len(ten_day_news),
        'current_days': days,
        'specific_date': specific_date,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'news/ten_day_news.html', context)
