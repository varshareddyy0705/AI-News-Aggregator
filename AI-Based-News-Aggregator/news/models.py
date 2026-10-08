from django.db import models
from django.utils import timezone


class Headline(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(null = True, blank = True)
    url = models.TextField()
    source = models.CharField(max_length=200,null = True,blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_live = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class EHeadline(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(null = True, blank = True)
    url = models.TextField()
    source = models.CharField(max_length=200,null = True,blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_live = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class SHeadline(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(null = True, blank = True)
    url = models.TextField()
    source = models.CharField(max_length=200,null = True,blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_live = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class PHeadline(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(null = True, blank = True)
    url = models.TextField()
    source = models.CharField(max_length=200,null = True,blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_live = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class LHeadline(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(null = True, blank = True)
    url = models.TextField()
    source = models.CharField(max_length=200,null = True,blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_live = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class ENHeadline(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(null = True, blank = True)
    url = models.TextField()
    source = models.CharField(max_length=200,null = True,blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_live = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']