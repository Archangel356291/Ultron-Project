"""Minimal fake of 'aiohttp' — enough to test bot.py's backend_get/backend_chat
without a real network connection."""


class ClientError(Exception):
    pass


class ClientTimeout:
    def __init__(self, total=None):
        self.total = total


class _MockResponse:
    def __init__(self, status, json_body=None, text_body="", headers=None):
        self.status = status
        self._json_body = json_body if json_body is not None else {}
        self._text_body = text_body
        self.headers = headers or {}

    async def json(self):
        return self._json_body

    async def text(self):
        return self._text_body

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False


class ClientSession:
    """Test double: configure `.script` with a queue of _MockResponse objects
    (or an Exception instance to raise) and each call to get()/post() will
    consume the next one."""
    def __init__(self):
        self.script = []
        self.calls = []
        self.closed = False

    def _next(self, method, url, **kwargs):
        self.calls.append({"method": method, "url": url, **kwargs})
        if not self.script:
            raise RuntimeError("fake aiohttp: script exhausted")
        item = self.script.pop(0)
        if isinstance(item, Exception):
            raise item
        return item

    def get(self, url, headers=None, timeout=None):
        return self._next("GET", url, headers=headers, timeout=timeout)

    def post(self, url, headers=None, json=None, timeout=None):
        return self._next("POST", url, headers=headers, json=json, timeout=timeout)

    async def close(self):
        self.closed = True
