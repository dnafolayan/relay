class PasswordProcessingException(Exception):
    def __init__(self, detail: str | None = None):
        if detail:
            self.message = f"Password processing failed: {detail}"
        else:
            self.message = "Password processing failed while registering the user."
        self.detail = detail
        super().__init__(self.message)
