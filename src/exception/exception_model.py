class UnauthorizedException(Exception):
    def __init__(self, message: str = ""):
        self.message = "Unauthorized access"
        if message != "":
            self.message = f"{self.message}: {message}"
        super().__init__(self.message)


class InputException(Exception):
    def __init__(self, message: str = ""):
        self.message = "Invalid input"
        if message != "":
            self.message = f"{self.message}: {message}"
        super().__init__(self.message)
