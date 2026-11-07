class SchoolAlreadyExistsException(Exception):
    def __init__(self, email: str, message: str):
        self.email = email
        self.message = f"School registration failed for email '{self.email}': {message}"
        super().__init__(self.message)
