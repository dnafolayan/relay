class SchoolRetrievalException(Exception):
    def __init__(self, email: str):
        self.email = email
        self.message = f"School retrieval failed for email {email}"
        super().__init__(self.message)
