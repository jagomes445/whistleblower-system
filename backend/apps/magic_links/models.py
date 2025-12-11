"""
MagicLink model for the whistleblower system.
"""
import uuid
from django.db import models
from django.utils import timezone


class MagicLink(models.Model):
    """
    MagicLink model for generating unique report submission links.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='magic_links'
    )
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='created_magic_links'
    )
    name = models.CharField(max_length=255, blank=True, help_text='Optional label for this magic link')
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'magic_links'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name or 'Unnamed'} - {self.token}"
    
    def is_valid(self):
        """
        Check if the magic link is currently valid.
        """
        if not self.is_active:
            return False
        
        if self.expires_at and self.expires_at < timezone.now():
            return False
        
        return True
