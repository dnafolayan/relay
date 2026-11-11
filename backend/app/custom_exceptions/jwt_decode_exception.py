class JwtDecodeException(Exception):
    """Custom exception for JWT decoding errors."""

    def __init__(self, message: str = "Error decoding JWT token"):
        self.message = message
        super().__init__(self.message)
