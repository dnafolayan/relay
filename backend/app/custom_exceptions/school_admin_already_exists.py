class SchoolAdminAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email
        self.message = f"Admin with email {email} already exists for the school"
        super().__init__(self.message)
