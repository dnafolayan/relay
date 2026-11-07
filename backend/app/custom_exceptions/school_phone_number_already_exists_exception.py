class SchoolPhoneNumberAlreadyExistsException(Exception):
    def __init__(self, phone_number: str, email: str):
        self.phone_number = phone_number
        self.email = email
        self.message = (
            f"School registration failed for school with email {email}: "
            f"phone number {phone_number} is already registered"
        )
        super().__init__(self.message)
