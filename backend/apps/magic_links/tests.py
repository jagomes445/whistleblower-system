"""
Tests for the magic_links app.
"""
import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from apps.companies.models import Company
from apps.magic_links.models import MagicLink

User = get_user_model()


@pytest.mark.django_db
class TestMagicLinkModel:
    """Test the MagicLink model."""
    
    def test_create_magic_link(self):
        """Test creating a magic link."""
        company = Company.objects.create(name="Test Company")
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            company=company
        )
        
        magic_link = MagicLink.objects.create(
            company=company,
            created_by=user,
            name="Test Link",
            is_active=True
        )
        
        assert magic_link.company == company
        assert magic_link.created_by == user
        assert magic_link.name == "Test Link"
        assert magic_link.is_active is True
        assert magic_link.token is not None
    
    def test_magic_link_is_valid(self):
        """Test magic link validation."""
        company = Company.objects.create(name="Test Company")
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            company=company
        )
        
        # Active link without expiration
        link1 = MagicLink.objects.create(
            company=company,
            created_by=user,
            is_active=True
        )
        assert link1.is_valid() is True
        
        # Inactive link
        link2 = MagicLink.objects.create(
            company=company,
            created_by=user,
            is_active=False
        )
        assert link2.is_valid() is False
        
        # Expired link
        link3 = MagicLink.objects.create(
            company=company,
            created_by=user,
            is_active=True,
            expires_at=timezone.now() - timedelta(days=1)
        )
        assert link3.is_valid() is False


@pytest.mark.django_db
class TestMagicLinkAPI:
    """Test magic link endpoints."""
    
    def test_list_magic_links(self):
        """Test listing magic links."""
        company = Company.objects.create(name="Test Company")
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            company=company
        )
        
        # Create some magic links
        MagicLink.objects.create(company=company, created_by=user, name="Link 1")
        MagicLink.objects.create(company=company, created_by=user, name="Link 2")
        
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.get("/api/magic-links/")
        assert response.status_code == 200
        assert len(response.data) == 2
    
    def test_create_magic_link(self):
        """Test creating a magic link."""
        company = Company.objects.create(name="Test Company")
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            company=company
        )
        
        client = APIClient()
        client.force_authenticate(user=user)
        
        data = {
            "name": "New Link",
            "is_active": True,
            "expires_at": None
        }
        
        response = client.post("/api/magic-links/", data)
        assert response.status_code == 201
        assert response.data["name"] == "New Link"
        assert "token" in response.data
    
    def test_data_segregation(self):
        """Test that users can only see their company's magic links."""
        company1 = Company.objects.create(name="Company 1")
        company2 = Company.objects.create(name="Company 2")
        
        user1 = User.objects.create_user(
            email="user1@example.com",
            password="pass123",
            first_name="User",
            last_name="One",
            company=company1
        )
        
        user2 = User.objects.create_user(
            email="user2@example.com",
            password="pass123",
            first_name="User",
            last_name="Two",
            company=company2
        )
        
        # Create magic links for both companies
        MagicLink.objects.create(company=company1, created_by=user1, name="Link 1")
        MagicLink.objects.create(company=company2, created_by=user2, name="Link 2")
        
        # User 1 should only see their company's link
        client = APIClient()
        client.force_authenticate(user=user1)
        
        response = client.get("/api/magic-links/")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Link 1"
