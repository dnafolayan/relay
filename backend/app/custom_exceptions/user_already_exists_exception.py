class UserAlreadyExistsException(Exception):
    def __init__(self, email: str, message: str):
        self.email = email
        self.message = (
            f"User registration failed for user with {self.email}: {self.message}"
        )
        super().__init__(self.message)
