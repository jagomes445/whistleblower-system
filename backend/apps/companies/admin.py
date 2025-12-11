from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('created_at',)
