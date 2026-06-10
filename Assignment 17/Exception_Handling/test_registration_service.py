import pytest
from registration_service import RegistrationService, InvalidEmailError, UnderageError

# --- Test Lifecycle Setup ---
@pytest.fixture
def service():
    """Provides a fresh RegistrationService instance before each test."""
    return RegistrationService()


# --- Unit Testing Suite ---
def test_successful_registration(service):
    # Should return True for a valid email and valid age
    result = service.register_user("john.doe@example.com", 25)
    assert result is True


def test_invalid_email_raises_error(service):
    # Verifies that an invalid email triggers the custom InvalidEmailError
    with pytest.raises(InvalidEmailError) as exc_info:
        service.register_user("johndoe-at-example", 20)
    
    assert "Invalid email format provided" in str(exc_info.value)


def test_underage_raises_error(service):
    # Verifies that a valid email but underage user triggers UnderageError
    with pytest.raises(UnderageError) as exc_info:
        service.register_user("john.doe@example.com", 16)
        
    assert "User must be at least 18" in str(exc_info.value)


def test_none_email_triggers_assertion_error(service):
    # Verifies that our internal assert statement catches None inputs
    with pytest.raises(AssertionError) as exc_info:
        service.register_user(None, 20)
        
    assert "Email cannot be None" in str(exc_info.value)