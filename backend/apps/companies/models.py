"""
Company model for the whistleblower system.
"""
import uuid
from django.db import models
from django.utils import timezone


class Company(models.Model):
    """
    Company model for managing organizations using the whistleblower system.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='created_companies',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'companies'
        verbose_name_plural = 'Companies'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
