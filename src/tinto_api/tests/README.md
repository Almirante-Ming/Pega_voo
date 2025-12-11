# Tinto API - Unit Tests

This directory contains comprehensive unit tests for all endpoints of the Tinto Booking API.

## Test Structure

The tests are organized by feature/endpoint:

- **test_authentication.py** - Tests for user registration and login endpoints
- **test_account_recovery.py** - Tests for password recovery functionality
- **test_flights.py** - Tests for flight search and retrieval endpoints
- **test_airlines.py** - Tests for airline endpoints
- **test_tickets.py** - Tests for ticket booking and management endpoints
- **test_persons.py** - Tests for person management endpoints (admin only)
- **test_health_resposnse.py** - Tests for health check endpoint
- **conftest.py** - Shared fixtures and pytest configuration

## Running the Tests

### Prerequisites

Make sure you have pytest and dependencies installed:

```bash
pip install pytest pytest-cov
```

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=tinto --cov-report=html
```

This generates an HTML coverage report in `htmlcov/index.html`.

### Run Specific Test File

```bash
pytest tests/test_authentication.py
```

### Run Specific Test Class

```bash
pytest tests/test_authentication.py::TestAuthentication
```

### Run Specific Test Function

```bash
pytest tests/test_authentication.py::TestAuthentication::test_register_person_success
```

### Run Tests with Verbose Output

```bash
pytest -v
```

### Run Tests and Stop on First Failure

```bash
pytest -x
```

### Run Tests by Marker

```bash
pytest -m "unit"
```

## Test Coverage

Current test coverage includes:

### Authentication
- ✅ User registration (success and failure cases)
- ✅ Duplicate email/CPF handling
- ✅ Login with email and phone number
- ✅ Password validation
- ✅ Invalid credentials handling

### Account Recovery
- ✅ Recovery code request by email and phone
- ✅ Recovery code validation
- ✅ Invalid identifier handling
- ✅ Expired code handling
- ✅ Password reset functionality

### Flights
- ✅ List all flights
- ✅ Retrieve specific flight
- ✅ Handle nonexistent flights
- ✅ Flight search

### Airlines
- ✅ List all airlines
- ✅ Retrieve specific airline
- ✅ IATA code lookup

### Tickets
- ✅ User ticket retrieval
- ✅ Ticket booking
- ✅ Ticket cancellation

### Persons (Admin)
- ✅ Authentication requirement checks
- ✅ Authorization tests

### Health Check
- ✅ API availability verification

## Test Data

Tests use fixtures from `conftest.py` to provide consistent test data:

- `test_user_data` - Standard test user
- `test_admin_data` - Admin user for privileged operations
- `test_flight_data` - Sample flight information
- `test_airline_data` - Sample airline information
- `unique_id` - UUID for generating unique test data

## Notes

- Tests use `TestClient` from FastAPI for HTTP requests
- Unique IDs are generated for each test to avoid conflicts
- Some tests are skipped if required data is not available in the database
- Protected endpoints require authentication tokens
- Admin-only endpoints check for proper authorization

## CI/CD Integration

To integrate these tests in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest --cov=tinto --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage.xml
```

## Future Improvements

- Add integration tests for complex workflows
- Add performance/load tests
- Implement test data factories for better data management
- Add API documentation tests
- Implement contract tests with mock services
