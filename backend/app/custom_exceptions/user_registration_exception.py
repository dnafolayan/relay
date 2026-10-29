class UserRegistrationException(Exception):
    def __init__(self, message: str | None = None, email: str | None = None):
        if email and message:
            self.message = f"User registration failed for email '{email}': {message}"
        elif email:
            self.message = f"User registration failed for email '{email}'."
        elif message:
            self.message = f"User registration failed: {message}"
        else:
            self.message = "User registration failed while creating the user account."

        self.email = email
        self.detail = message
        super().__init__(self.message)
