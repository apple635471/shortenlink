"""exceptions about shortenlink"""


class ShortenURLCreationError(Exception):
    def __init__(self, msg: str | None = None):
        self.msg = msg if msg else "Failed to create shorten URL"

    def __str__(self):
        return self.msg


class ShortenURLRetrievalError(Exception):
    def __init__(self, msg: str | None = None):
        self.msg = msg if msg else "Failed to retrieve shorten URL"

    def __str__(self):
        return self.msg


class TrackingCreationError(Exception):
    def __init__(self, msg: str | None = None):
        self.msg = msg if msg else "Failed to create tracking record"

    def __str__(self):
        return self.msg


class URLRetrievalError(Exception):
    def __init__(self, msg: str | None = None):
        self.msg = msg if msg else "Failed to retrieve URL"

    def __str__(self):
        return self.msg
