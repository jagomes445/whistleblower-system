"""
Report model for the whistleblower system.
"""
import uuid
from django.db import models
from django.utils import timezone
from core.utils import encrypt_field, decrypt_field


class Report(models.Model):
    """
    Report model for storing whistleblower reports.
    """
    CATEGORY_CHOICES = [
        ('harassment', 'Harassment'),
        ('fraud', 'Fraud'),
        ('safety', 'Safety'),
        ('discrimination', 'Discrimination'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_review', 'In Review'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    magic_link = models.ForeignKey(
        'magic_links.MagicLink',
        on_delete=models.CASCADE,
        related_name='reports'
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    is_anonymous = models.BooleanField(default=True)
    _reporter_name = models.TextField(null=True, blank=True, db_column='reporter_name')
    _reporter_email = models.TextField(null=True, blank=True, db_column='reporter_email')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    internal_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_category_display()} - {self.created_at.strftime('%Y-%m-%d')}"
    
    @property
    def reporter_name(self):
        """Decrypt and return reporter name."""
        if self._reporter_name:
            return decrypt_field(self._reporter_name)
        return None
    
    @reporter_name.setter
    def reporter_name(self, value):
        """Encrypt and set reporter name."""
        if value:
            self._reporter_name = encrypt_field(value)
        else:
            self._reporter_name = None
    
    @property
    def reporter_email(self):
        """Decrypt and return reporter email."""
        if self._reporter_email:
            return decrypt_field(self._reporter_email)
        return None
    
    @reporter_email.setter
    def reporter_email(self, value):
        """Encrypt and set reporter email."""
        if value:
            self._reporter_email = encrypt_field(value)
        else:
            self._reporter_email = None
