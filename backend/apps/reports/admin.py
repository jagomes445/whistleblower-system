from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'status', 'is_anonymous', 'magic_link', 'created_at')
    list_filter = ('status', 'category', 'is_anonymous', 'created_at')
    search_fields = ('description', 'internal_notes')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Report Information', {
            'fields': ('id', 'magic_link', 'category', 'description', 'is_anonymous')
        }),
        ('Reporter Information', {
            'fields': ('_reporter_name', '_reporter_email'),
            'description': 'Encrypted fields - handle with care'
        }),
        ('Management', {
            'fields': ('status', 'internal_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
