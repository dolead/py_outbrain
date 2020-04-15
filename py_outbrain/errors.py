class OutbrainError(BaseException):
    """
    Base error class for handling Outbrain backstage API errors
    """

    def __init__(self, error, response):
        self.error = error
        self.response = response
        super().__init__()

    def __str__(self):
        return '{} [{}]: {}'.format(self.__class__.__name__,
                                    self.response.status_code,
                                    self.error)


class BadRequest(OutbrainError):
    """
    400 HTTP Errors
    """


class Unauthorized(OutbrainError):
    """
    401 HTTP Errors
    """


class NotFound(OutbrainError):
    """
    404 HTTP Errors
    """


class TooManyRequests(OutbrainError):
    """
    429 HTTP Errors
    """

    def __init__(self, error, response):
        super().__init__(error, response)
        try:
            self.rate_limit_msec_left = int(
                    response.headers['rate-limit-msec-left'])
        except (TypeError, ValueError, KeyError):
            self.rate_limit_msec_left = 0


class ServerError(OutbrainError):
    """
    500 HTTP Errors
    """


class TooManyAuthRequests(TooManyRequests):
    """
    429 HTTP Errors for token requests
    """
