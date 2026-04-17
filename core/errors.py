class OriginLanguageError(Exception):
    error_type = "OriginError"

    def __init__(self, message, line=None, column=None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        res = ""
        if self.line is not None:
            res += f"[{self.line}:{self.column}] "
        res += self.message
        return res


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
