class ClientOptions:
    def __init__(self, auth: str, url: str, timeout=0.0):
        self.auth = auth
        self.timeout = timeout
        self.url = url
