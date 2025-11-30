# Testing Documentation

## Overview
This document describes the testing strategy and procedures for the Django REST Framework API.

## Test Structure
- **Location**: `api/tests_views.py`
- **Framework**: Django Test Framework (based on Python unittest)
- **Database**: Separate test database (SQLite in memory)

## Test Categories

### 1. CRUD Operations
- **Create**: Test book/author creation with valid and invalid data
- **Read**: Test listing and retrieving individual books/authors
- **Update**: Test full and partial updates
- **Delete**: Test deletion with proper permissions

### 2. Filtering, Searching, and Ordering
- **Filtering**: By publication year, author name, title
- **Searching**: Full-text search across title and author fields
- **Ordering**: Ascending/descending by various fields

### 3. Authentication and Permissions
- **Unauthorized access**: Ensure proper restriction
- **Authorized access**: Verify functionality for authenticated users
- **Permission enforcement**: Check role-based access control

## Running Tests

### Run All Tests
```bash
python manage.py test api