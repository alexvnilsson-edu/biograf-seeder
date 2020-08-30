class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class DbConnectionError(Error):
    def __init__(self, message, errors=None):
        self.message = message
        self.errors = errors
        super(DbConnectionError, self).__init__(message)


class DbQueryError(Error):
    def __init__(self, message, errors=None):
        self.message = message
        self.errors = errors
        super(DbQueryError, self).__init__(message)


class NotFoundError(Error):
    def __init__(self, message, errors=None):
        self.message = message
        self.errors = errors
        super(NotFoundError, self).__init__(message)
