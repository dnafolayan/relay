class UserAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email
        self.message = f"User registration failed: a user with email '{self.email}' already exists."
        super().__init__(self.message)
