from django.contrib import admin
from .models import MagicLink


@admin.register(MagicLink)
class MagicLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'token', 'company', 'created_by', 'is_active', 'expires_at', 'created_at')
    list_filter = ('is_active', 'created_at', 'expires_at')
    search_fields = ('name', 'token', 'company__name')
    readonly_fields = ('id', 'token', 'created_at')
