class LoginException(Exception):
    def __init__(self, *args, field=None) -> None:
        self.exception_field=field
        super().__init__(*args)

    def __str__(self) -> str:
        print(self.exception_field)
        if self.exception_field == "username":
            return "Invalid username"
        else:
            return "Invalid password"