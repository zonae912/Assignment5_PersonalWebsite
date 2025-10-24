#!/bin/bash
# Run All Tests Script (Linux/Mac)
# Quick script to run all tests with coverage

echo "Running Flask Website Test Suite..."
echo ""

# Run all tests with coverage
pytest --cov=. --cov-report=html --cov-report=term-missing -v

echo ""
echo "Test run complete!"
echo "Coverage report generated in htmlcov/index.html"
