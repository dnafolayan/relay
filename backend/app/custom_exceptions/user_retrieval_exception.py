class UserRetrievalException(Exception):
    def __init__(self, email: str):
        self.email = email
        self.message = f"User retrieval failed for email {email}"
        super().__init__(self.message)
