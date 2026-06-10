import re

# --- Custom Exception Design ---
class InvalidEmailError(ValueError):
    """Raised when the email does not match the required format."""
    def __init__(self, email: str):
        # Dynamic error message based on input
        super().__init__(f"Invalid email format provided: '{email}'")

class UnderageError(ValueError):
    """Raised when the applicant is under 18."""
    def __init__(self, age: int):
        super().__init__(f"Registration denied: User must be at least 18. Provided age: {age}")


# --- Core Service Validation ---
class RegistrationService:
    # Regex pattern: Valid identifier + @ + domain name
    EMAIL_REGEX = re.compile(r"^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}$")

    def register_user(self, email: str, age: int) -> bool:
        # Internal invariant assertion: Email should never be None at this stage
        assert email is not None, "System constraint failed: Email cannot be None at processing stage"

        # 1. Validate Email string (not empty and matches regex)
        if not email.strip() or not self.EMAIL_REGEX.match(email):
            raise InvalidEmailError(email)

        # 2. Validate Age boundary
        if age < 18:
            raise UnderageError(age)

        # Registration is successful if no exceptions are raised
        return True


# --- THIS BLOCK MUST START AT THE FAR LEFT OUTSIDE THE CLASS ---
if __name__ == "__main__":
    service = RegistrationService()
    
    try:
        # Testing with an underage user (16) to see if our custom exception triggers
        result = service.register_user("john.doe@example.com", 16)

        if result:
            print("Registration successful!")   

    except (InvalidEmailError, UnderageError) as e:
        print(f"❌ Custom Error Caught: {e}")