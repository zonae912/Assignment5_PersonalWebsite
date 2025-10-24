# Testing Guide for Flask Personal Website

This guide explains how to run the pytest test suite for your Flask application.

## Prerequisites

Install the testing dependencies:
```powershell
pip install -r requirements.txt
```

Or install pytest separately:
```powershell
pip install pytest pytest-cov
```

## Test Files

The test suite includes:

1. **`conftest.py`** - Pytest configuration and shared fixtures
   - App and client fixtures for testing
   - Test database fixtures
   - Sample data fixtures

2. **`test_dal.py`** - Data Access Layer (DAL) tests
   - Database initialization tests
   - CRUD operation tests (Create, Read, Update, Delete)
   - Project search and filtering tests

3. **`test_routes.py`** - Flask route integration tests
   - Static page route tests
   - Form submission tests
   - Database integration tests
   - Error handling tests

## Running Tests

### Run all tests:
```powershell
pytest
```

### Run specific test file:
```powershell
pytest test_dal.py
pytest test_routes.py
```

### Run specific test class:
```powershell
pytest test_dal.py::TestAddProject
pytest test_routes.py::TestContactRoute
```

### Run specific test function:
```powershell
pytest test_dal.py::TestAddProject::test_add_project_with_all_fields
```

### Run with verbose output:
```powershell
pytest -v
```

### Run with coverage report:
```powershell
pytest --cov=. --cov-report=html
```
This generates an HTML coverage report in `htmlcov/index.html`

### Run and show print statements:
```powershell
pytest -s
```

### Run only failed tests from last run:
```powershell
pytest --lf
```

### Stop at first failure:
```powershell
pytest -x
```

## Test Coverage

To see which parts of your code are tested:

```powershell
pytest --cov=. --cov-report=term-missing
```

This shows:
- Percentage of code covered by tests
- Line numbers that aren't tested

## Understanding Test Output

### Successful test:
```
test_dal.py::TestAddProject::test_add_project_with_all_fields PASSED [100%]
```

### Failed test:
```
test_dal.py::TestAddProject::test_add_project_with_all_fields FAILED [100%]
```
Followed by detailed error information.

## Test Structure

### Fixtures (in conftest.py)
Fixtures provide reusable test components:
- `app` - Flask application instance
- `client` - Test client for making requests
- `test_dal` - Isolated test database
- `sample_project_data` - Sample project data
- `populated_dal` - Pre-populated test database

### Test Classes
Tests are organized by functionality:
- `TestDALInitialization` - Database setup
- `TestAddProject` - Adding projects
- `TestGetAllProjects` - Retrieving projects
- `TestUpdateProject` - Updating projects
- `TestDeleteProject` - Deleting projects
- `TestStaticRoutes` - Static page routes
- `TestContactRoute` - Contact form
- `TestAddProjectRoute` - Add project form

## Writing New Tests

### Example test function:
```python
def test_my_feature(client, test_dal):
    """Test description"""
    # Arrange - Set up test data
    project_id = test_dal.add_project(
        title='Test',
        description='Test Desc',
        image_filename='test.jpg'
    )
    
    # Act - Perform the action
    response = client.get('/projects')
    
    # Assert - Verify the result
    assert response.status_code == 200
    assert b'Test' in response.data
```

## Common Test Patterns

### Testing GET requests:
```python
def test_get_route(client):
    response = client.get('/about')
    assert response.status_code == 200
```

### Testing POST requests:
```python
def test_post_route(client):
    response = client.post('/contact', data={
        'firstName': 'John',
        'lastName': 'Doe'
    })
    assert response.status_code == 200
```

### Testing database operations:
```python
def test_database_operation(test_dal):
    project_id = test_dal.add_project(
        title='Test',
        description='Desc',
        image_filename='img.jpg'
    )
    assert project_id > 0
```

### Testing with redirects:
```python
def test_redirect(client):
    response = client.post('/contact', data={...}, follow_redirects=True)
    assert response.request.path == '/thankyou'
```

## Continuous Integration

For CI/CD pipelines, run:
```powershell
pytest --cov=. --cov-report=xml --junitxml=test-results.xml
```

## Troubleshooting

### Import errors:
Make sure pytest is installed:
```powershell
pip install pytest pytest-cov
```

### Database locked errors:
Tests use temporary databases, but if you see this error, ensure:
- No other processes are using the test database
- Tests properly close database connections

### Fixture not found:
Ensure `conftest.py` is in the same directory as your tests.

### Tests not discovered:
- Test files must start with `test_`
- Test functions must start with `test_`
- Test classes must start with `Test`

## Best Practices

1. **Keep tests isolated** - Each test should be independent
2. **Use fixtures** - Share setup code via fixtures
3. **Test one thing** - Each test should verify one behavior
4. **Use descriptive names** - Test names should explain what they test
5. **Arrange-Act-Assert** - Follow the AAA pattern
6. **Clean up** - Use fixtures to handle cleanup automatically

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Flask Testing](https://flask.palletsprojects.com/en/latest/testing/)
- [Testing Best Practices](https://docs.pytest.org/en/latest/goodpractices.html)
