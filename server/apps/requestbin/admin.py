from django.contrib import admin

from .models import Request, Bin


@admin.register(Bin)
class BinAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['url', 'ip', 'method', 'start_time', 'finish_time', 'ip']
