class SchoolAlreadyExistsException(Exception):
    def __init__(self, email: str, message: str):
        self.email = email
        self.message = (
            f"School registration failed for school with {self.email}: {self.message}"
        )
        super().__init__(self.message)
