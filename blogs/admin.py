from django.contrib import admin
from .models import *


# Register your models here.

class BlogsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_created',)
    list_display_links = ('title',)
    search_fields = ('title', 'author',)
    list_filter = ('title', 'author', 'date_created',)


class SubscribersAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to']


admin.site.register(Blogs, BlogsAdmin)
admin.site.register(Subscribers, SubscribersAdmin)