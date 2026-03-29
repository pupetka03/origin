class OriginLanguageError(Exception):
    error_type = "OriginError"

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class OriginSyntaxError(OriginLanguageError):
    error_type = "SyntaxError"


class OriginNameError(OriginLanguageError):
    error_type = "NameError"


class OriginTypeError(OriginLanguageError):
    error_type = "TypeError"


class OriginRuntimeError(OriginLanguageError):
    error_type = "RuntimeError"


class OriginFileError(OriginLanguageError):
    error_type = "FileError"


def format_origin_error(error):
    return f"{error.error_type}: {error}"
