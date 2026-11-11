class InvalidLoginException(Exception):
    """Custom exception for invalid login attempts."""

    def __init__(self, message: str = "Invalid login credentials"):
        self.message = message
        super().__init__(self.message)
