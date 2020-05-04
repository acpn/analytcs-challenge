from django.db import models
from jsonfield import JSONField

class User(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=320)
    password = models.CharField(max_length=20)
    gender = models.CharField(max_length=50, default='N/A')
    credentials = JSONField(null=True)

    def __str__(self):
        return self.full_name

class AnalyticsAccount(models.Model):
    user_id = models.IntegerField()
    owner = models.CharField(max_length=500, null=True)
    accountid = models.IntegerField()
    name = models.CharField(max_length=300)
    permissions = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class AnalyticsProperties(models.Model):
    accountid = models.ForeignKey(AnalyticsAccount, on_delete=models.CASCADE)
    propid = models.CharField(max_length=100)
    name = models.CharField(max_length=300)
    level = models.CharField(max_length=20)
    site = models.CharField(max_length=500)
    industry = models.CharField(max_length=50)
    userid = models.IntegerField()
    
    def __str__(self):
        return self.name

class AnalyticsViews(models.Model):
    propid = models.ForeignKey(AnalyticsProperties, on_delete=models.CASCADE)
    viewid = models.IntegerField()
    viewname = models.CharField(max_length=500)
    currency = models.CharField(max_length=3)
    created = models.DateTimeField(null=True)
    updated = models.DateTimeField(null=True)
    timezone = models.CharField(max_length=200)
    userid = models.IntegerField()
    
    def __str__(self):
        return self.viewname

class LogEvents(models.Model):
    userid = models.IntegerField()
    logdescription = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    timeresponse = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.logdescription