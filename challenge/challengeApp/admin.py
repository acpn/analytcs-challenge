from django.contrib import admin
from .models import User, AnalyticsAccount, \
    AnalyticsProperties, AnalyticsViews, LogEvents

admin.site.register(User)
admin.site.register(AnalyticsAccount)
admin.site.register(AnalyticsProperties)
admin.site.register(AnalyticsViews)
admin.site.register(LogEvents)