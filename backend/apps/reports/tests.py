"""
Tests for the reports app.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.companies.models import Company
from apps.magic_links.models import MagicLink
from apps.reports.models import Report

User = get_user_model()


@pytest.mark.django_db
class TestReportModel:
    """Test the Report model."""
    
    def test_create_anonymous_report(self):
        """Test creating an anonymous report."""
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
            created_by=user
        )
        
        report = Report.objects.create(
            magic_link=magic_link,
            category="harassment",
            description="Test report description",
            is_anonymous=True,
            status="new"
        )
        
        assert report.magic_link == magic_link
        assert report.category == "harassment"
        assert report.is_anonymous is True
        assert report.status == "new"
        assert report.reporter_name is None
        assert report.reporter_email is None
    
    def test_create_named_report_with_encryption(self):
        """Test creating a named report with encrypted info."""
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
            created_by=user
        )
        
        report = Report.objects.create(
            magic_link=magic_link,
            category="fraud",
            description="Test report description",
            is_anonymous=False,
            status="new"
        )
        
        # Set encrypted fields
        report.reporter_name = "John Doe"
        report.reporter_email = "john@example.com"
        report.save()
        
        # Reload from database
        report.refresh_from_db()
        
        # Check that encryption/decryption works
        assert report.reporter_name == "John Doe"
        assert report.reporter_email == "john@example.com"
        
        # Check that the database stores encrypted data
        assert report._reporter_name != "John Doe"
        assert report._reporter_email != "john@example.com"


@pytest.mark.django_db
class TestReportAPI:
    """Test report endpoints."""
    
    def test_list_reports(self):
        """Test listing reports."""
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
            created_by=user
        )
        
        # Create some reports
        Report.objects.create(
            magic_link=magic_link,
            category="harassment",
            description="Report 1"
        )
        Report.objects.create(
            magic_link=magic_link,
            category="fraud",
            description="Report 2"
        )
        
        client = APIClient()
        client.force_authenticate(user=user)
        
        response = client.get("/api/reports/")
        assert response.status_code == 200
        # Response might be paginated
        if isinstance(response.data, dict) and 'results' in response.data:
            assert len(response.data['results']) == 2
        else:
            assert len(response.data) == 2
    
    def test_update_report_status(self):
        """Test updating report status."""
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
            created_by=user
        )
        report = Report.objects.create(
            magic_link=magic_link,
            category="harassment",
            description="Test report",
            status="new"
        )
        
        client = APIClient()
        client.force_authenticate(user=user)
        
        data = {
            "status": "in_review",
            "internal_notes": "Started investigation"
        }
        
        response = client.put(f"/api/reports/{report.id}/", data)
        assert response.status_code == 200
        assert response.data["status"] == "in_review"
        assert response.data["internal_notes"] == "Started investigation"
    
    def test_public_report_submission(self):
        """Test submitting a report via magic link."""
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
            is_active=True
        )
        
        client = APIClient()
        data = {
            "category": "safety",
            "description": "Unsafe working conditions",
            "is_anonymous": True
        }
        
        response = client.post(
            f"/api/reports/public/{magic_link.token}/submit/",
            data
        )
        assert response.status_code == 201
        assert "report_id" in response.data
        
        # Check report was created
        report = Report.objects.get(id=response.data["report_id"])
        assert report.category == "safety"
        assert report.is_anonymous is True
    
    def test_data_segregation_reports(self):
        """Test that users can only see their company's reports."""
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
        
        link1 = MagicLink.objects.create(company=company1, created_by=user1)
        link2 = MagicLink.objects.create(company=company2, created_by=user2)
        
        Report.objects.create(magic_link=link1, category="fraud", description="Report 1")
        Report.objects.create(magic_link=link2, category="fraud", description="Report 2")
        
        # User 1 should only see their company's report
        client = APIClient()
        client.force_authenticate(user=user1)
        
        response = client.get("/api/reports/")
        assert response.status_code == 200
        
        # Handle paginated response
        if isinstance(response.data, dict) and 'results' in response.data:
            results = response.data['results']
        else:
            results = response.data
        
        assert len(results) == 1
        assert results[0]["description"] == "Report 1"
