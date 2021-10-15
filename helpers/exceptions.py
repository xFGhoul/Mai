class MaiBaseException(Exception):
    """Base Exception Used For Mai Errors"""


class LanguageNotSupportedError(MaiBaseException):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotDeveloperError(MaiBaseException):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class GuildIsBlacklistedError(MaiBaseException):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class ChannelIsBlacklistedError(MaiBaseException):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class UserIsBlacklistedError(MaiBaseException):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
