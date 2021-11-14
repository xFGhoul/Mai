"""API Exceptions"""


class MaiAPIBaseException(BaseException):
    """Base Exception For Mai Backend API"""


class UserIsBlacklisted(MaiAPIBaseException):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class GuildIsBlacklisted(MaiAPIBaseException):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
