class AuthServiceUnavailableException(Exception):
    """Exception raised when the authentication service is unavailable."""

    def __init__(self, message: str = "Authentication service unavailable"):
        self.message = message
        super().__init__(self.message)
