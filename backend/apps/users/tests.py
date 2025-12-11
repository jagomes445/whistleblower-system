"""
Tests for the users app.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.companies.models import Company

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Test the User model."""
    
    def test_create_user(self):
        """Test creating a user."""
        company = Company.objects.create(name="Test Company")
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            company=company
        )
        
        assert user.email == "test@example.com"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.company == company
        assert user.check_password("testpass123")
        assert user.is_active is True
        assert user.is_staff is False
    
    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123",
            first_name="Admin",
            last_name="User"
        )
        
        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.role == "admin"


@pytest.mark.django_db
class TestAuthenticationAPI:
    """Test authentication endpoints."""
    
    def test_register_user(self):
        """Test user registration."""
        client = APIClient()
        data = {
            "email": "newuser@example.com",
            "password": "newpass123",
            "password_confirm": "newpass123",
            "first_name": "New",
            "last_name": "User",
            "company_name": "New Company"
        }
        
        response = client.post("/api/auth/register/", data)
        assert response.status_code == 201
        
        # Check user was created
        user = User.objects.get(email="newuser@example.com")
        assert user.first_name == "New"
        assert user.company is not None
        assert user.company.name == "New Company"
    
    def test_login_user(self):
        """Test user login."""
        # Create a user
        company = Company.objects.create(name="Test Company")
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            company=company
        )
        
        client = APIClient()
        data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        response = client.post("/api/auth/login/", data)
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data
    
    def test_get_user_profile(self):
        """Test getting user profile."""
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
        
        response = client.get("/api/auth/me/")
        assert response.status_code == 200
        assert response.data["email"] == "test@example.com"
        assert response.data["company_name"] == "Test Company"
