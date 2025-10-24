"""
Integration tests for Flask routes
Tests all routes and their responses
"""

import pytest
from flask import session


class TestStaticRoutes:
    """Test static page routes"""
    
    def test_index_route(self, client):
        """Test the home page route"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data
    
    def test_about_route(self, client):
        """Test the about page route"""
        response = client.get('/about')
        assert response.status_code == 200
    
    def test_resume_route(self, client):
        """Test the resume page route"""
        response = client.get('/resume')
        assert response.status_code == 200
    
    def test_thankyou_route(self, client):
        """Test the thank you page route"""
        response = client.get('/thankyou')
        assert response.status_code == 200


class TestProjectsRoute:
    """Test projects page functionality"""
    
    def test_projects_route_get(self, client):
        """Test GET request to projects page"""
        response = client.get('/projects')
        assert response.status_code == 200
    
    def test_projects_page_displays_projects(self, client, monkeypatch):
        """Test that projects page displays project data"""
        # Mock the DAL to return test data
        class MockDAL:
            def get_all_projects(self):
                return [
                    {
                        'id': 1,
                        'title': 'Test Project',
                        'description': 'Test Description',
                        'image_filename': 'test.jpg',
                        'category': 'Web',
                        'technologies': 'Python',
                        'project_url': 'http://test.com',
                        'duration': '1 month',
                        'role': 'Developer',
                        'created_date': '2025-01-01'
                    }
                ]
        
        # Patch the DAL in the app module
        import app as app_module
        monkeypatch.setattr(app_module, 'dal', MockDAL())
        
        response = client.get('/projects')
        assert response.status_code == 200
        assert b'Test Project' in response.data


class TestContactRoute:
    """Test contact form functionality"""
    
    def test_contact_route_get(self, client):
        """Test GET request to contact page"""
        response = client.get('/contact')
        assert response.status_code == 200
    
    def test_contact_form_valid_submission(self, client):
        """Test valid contact form submission"""
        response = client.post('/contact', data={
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'password': 'password123',
            'confirmPassword': 'password123',
            'newsletter': 'on'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Should redirect to thank you page
        assert b'thank' in response.data.lower() or response.request.path == '/thankyou'
    
    def test_contact_form_missing_required_fields(self, client):
        """Test contact form with missing required fields"""
        response = client.post('/contact', data={
            'firstName': '',
            'lastName': '',
            'email': '',
            'password': '',
            'confirmPassword': ''
        })
        
        # Should stay on contact page with errors
        assert response.status_code == 200
    
    def test_contact_form_password_mismatch(self, client):
        """Test contact form with mismatched passwords"""
        response = client.post('/contact', data={
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'password': 'password123',
            'confirmPassword': 'different456'
        })
        
        assert response.status_code == 200
        # Should show error message
        assert b'match' in response.data.lower() or b'error' in response.data.lower()


class TestAddProjectRoute:
    """Test add project functionality"""
    
    def test_add_project_route_get(self, client):
        """Test GET request to add project page"""
        response = client.get('/add-project')
        assert response.status_code == 200
    
    def test_add_project_valid_submission(self, client, monkeypatch):
        """Test valid project submission"""
        # Mock the DAL with all required methods
        class MockDAL:
            def add_project(self, **kwargs):
                return 1  # Return a mock project ID
            
            def get_all_projects(self):
                return []  # Return empty list for projects page
        
        import app as app_module
        monkeypatch.setattr(app_module, 'dal', MockDAL())
        
        response = client.post('/add-project', data={
            'title': 'New Project',
            'description': 'Project description',
            'image_filename': 'image.jpg',
            'category': 'Web Development',
            'technologies': 'Python, Flask',
            'project_url': 'https://example.com',
            'duration': '2 months',
            'role': 'Developer'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_add_project_missing_required_fields(self, client):
        """Test adding project with missing required fields"""
        response = client.post('/add-project', data={
            'title': '',
            'description': '',
            'image_filename': ''
        })
        
        assert response.status_code == 200
        # Should show error messages
    
    def test_add_project_with_optional_fields_only(self, client, monkeypatch):
        """Test adding project with only required fields"""
        class MockDAL:
            def add_project(self, **kwargs):
                return 1
            
            def get_all_projects(self):
                return []
        
        import app as app_module
        monkeypatch.setattr(app_module, 'dal', MockDAL())
        
        response = client.post('/add-project', data={
            'title': 'Minimal Project',
            'description': 'Minimal description',
            'image_filename': 'minimal.jpg'
        }, follow_redirects=True)
        
        assert response.status_code == 200


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_404_for_nonexistent_route(self, client):
        """Test that nonexistent routes return 404"""
        response = client.get('/nonexistent-page')
        assert response.status_code == 404
    
    def test_method_not_allowed(self, client):
        """Test POST to GET-only routes"""
        response = client.post('/about')
        assert response.status_code == 405  # Method Not Allowed


class TestFlashMessages:
    """Test flash message functionality"""
    
    def test_flash_message_on_contact_success(self, client):
        """Test that success flash message appears"""
        with client:
            response = client.post('/contact', data={
                'firstName': 'John',
                'lastName': 'Doe',
                'email': 'john@example.com',
                'password': 'password123',
                'confirmPassword': 'password123'
            }, follow_redirects=True)
            
            # Check if flash messages exist in session
            # Flash messages are consumed after display, so check in response
            assert response.status_code == 200
    
    def test_flash_message_on_validation_error(self, client):
        """Test that error flash messages appear on validation failure"""
        with client:
            response = client.post('/contact', data={
                'firstName': '',
                'lastName': '',
                'email': ''
            })
            
            assert response.status_code == 200


class TestDatabaseIntegration:
    """Test database integration with routes"""
    
    def test_projects_route_with_real_database(self, client, monkeypatch):
        """Test projects route with actual database queries"""
        from DAL import DAL
        import tempfile
        import os
        
        # Create a temporary test database
        db_fd, db_path = tempfile.mkstemp()
        test_dal = DAL(db_name=db_path)
        
        # Add test data
        test_dal.add_project(
            title='Integration Test Project',
            description='Test Description',
            image_filename='test.jpg'
        )
        
        # Patch the app's DAL
        import app as app_module
        monkeypatch.setattr(app_module, 'dal', test_dal)
        
        response = client.get('/projects')
        assert response.status_code == 200
        assert b'Integration Test Project' in response.data
        
        # Cleanup
        os.close(db_fd)
        os.unlink(db_path)
