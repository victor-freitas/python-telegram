from django.contrib import admin

from .models import TelegramApp

@admin.register(TelegramApp)
class ValidateAdmin(admin.ModelAdmin):
    list_display = ("name", "api_id", "api_hash", "date_created")



