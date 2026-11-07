class PasswordProcessingException(Exception):
    def __init__(self, message: str):
        self.message = f"Password processing failed: {message}"
        super().__init__(self.message)
