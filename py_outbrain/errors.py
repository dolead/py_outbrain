class OutbrainError(BaseException):
    """
    Base error class for handling Outbrain backstage API errors
    """

    def __init__(self, error, response):
        self.error = error
        self.response = response

    def __str__(self):
        return '{} [{}]: {}'.format(self.__class__.__name__,
                                    self.response.status_code,
                                    self.error)


class BadRequest(OutbrainError):
    """
    400 HTTP Errors
    """
    pass


class Unauthorized(OutbrainError):
    """
    401 HTTP Errors
    """
    pass


class NotFound(OutbrainError):
    """
    404 HTTP Errors
    """
    pass


class TooManyRequests(OutbrainError):
    """
    429 HTTP Errors
    """
    pass


class ServerError(OutbrainError):
    """
    500 HTTP Errors
    """
    pass
