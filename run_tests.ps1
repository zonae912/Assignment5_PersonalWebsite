# Run All Tests Script
# Quick script to run all tests with coverage

Write-Host "Running Flask Website Test Suite..." -ForegroundColor Green
Write-Host ""

# Run all tests with coverage
pytest --cov=. --cov-report=html --cov-report=term-missing -v

Write-Host ""
Write-Host "Test run complete!" -ForegroundColor Green
Write-Host "Coverage report generated in htmlcov/index.html" -ForegroundColor Cyan
