"""
Pytest configuration and fixtures for Flask application testing
"""

import pytest
import os
import tempfile
from app import app as flask_app
from DAL import DAL


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    flask_app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key',
        'WTF_CSRF_ENABLED': False  # Disable CSRF for testing
    })
    
    yield flask_app
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def test_dal():
    """Create a test DAL with a temporary database."""
    db_fd, db_path = tempfile.mkstemp()
    dal = DAL(db_name=db_path)
    
    yield dal
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def sample_project_data():
    """Sample project data for testing."""
    return {
        'title': 'Test Project',
        'description': 'This is a test project description',
        'image_filename': 'test_image.jpg',
        'category': 'Web Development',
        'technologies': 'Python, Flask, SQLite',
        'project_url': 'https://example.com',
        'duration': '3 months',
        'role': 'Full Stack Developer'
    }


@pytest.fixture
def populated_dal(test_dal, sample_project_data):
    """DAL with sample projects already added."""
    # Add multiple projects
    test_dal.add_project(**sample_project_data)
    
    test_dal.add_project(
        title='Second Project',
        description='Another test project',
        image_filename='project2.jpg',
        category='Data Science',
        technologies='Python, Pandas, NumPy'
    )
    
    test_dal.add_project(
        title='Third Project',
        description='Yet another test project',
        image_filename='project3.jpg',
        category='Machine Learning',
        technologies='Python, TensorFlow, Keras'
    )
    
    return test_dal
