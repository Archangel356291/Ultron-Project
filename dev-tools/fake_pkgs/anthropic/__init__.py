"""Fake stand-in for the real 'anthropic' package, used only for local
testing where network access to install the real SDK isn't available.
Mirrors the shapes documented at platform.claude.com: response.content is a
list of blocks (type == 'text' -> .text; type == 'tool_use' -> .id/.name/.input),
response.stop_reason is 'tool_use' or 'end_turn', and blocks support
.model_dump() for serialization."""


class APIError(Exception):
    pass


class APIConnectionError(APIError):
    pass


class APITimeoutError(APIConnectionError):
    pass


class APIStatusError(APIError):
    def __init__(self, message="", status_code=500):
        super().__init__(message)
        self.status_code = status_code


class BadRequestError(APIStatusError):
    def __init__(self, message=""):
        super().__init__(message, status_code=400)


class AuthenticationError(APIStatusError):
    def __init__(self, message=""):
        super().__init__(message, status_code=401)


class PermissionDeniedError(APIStatusError):
    def __init__(self, message=""):
        super().__init__(message, status_code=403)


class NotFoundError(APIStatusError):
    def __init__(self, message=""):
        super().__init__(message, status_code=404)


class RateLimitError(APIStatusError):
    def __init__(self, message=""):
        super().__init__(message, status_code=429)


class InternalServerError(APIStatusError):
    def __init__(self, message="", status_code=500):
        super().__init__(message, status_code=status_code)


class ContentBlock:
    def __init__(self, type, text=None, id=None, name=None, input=None):
        self.type = type
        self.text = text
        self.id = id
        self.name = name
        self.input = input or {}

    def model_dump(self):
        if self.type == "text":
            return {"type": "text", "text": self.text}
        if self.type == "tool_use":
            return {"type": "tool_use", "id": self.id, "name": self.name, "input": self.input}
        return {"type": self.type}


class Usage:
    def __init__(self, input_tokens=0, output_tokens=0, cache_read_input_tokens=0, cache_creation_input_tokens=0):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.cache_read_input_tokens = cache_read_input_tokens
        self.cache_creation_input_tokens = cache_creation_input_tokens


class Message:
    def __init__(self, content, stop_reason, usage=None):
        self.content = content
        self.stop_reason = stop_reason
        self.usage = usage or Usage()


class _MessagesAPI:
    def __init__(self):
        self.script = []   # test harness populates this with Message objects
        self.calls = []     # records every kwargs dict passed to create()
        self.raise_on_call = None

    def create(self, **kwargs):
        # Snapshot the messages list at call time — app.py mutates the same
        # list object across loop iterations, so without this every stored
        # call would end up showing the final state, not what was sent.
        snapshot = dict(kwargs)
        if "messages" in snapshot:
            snapshot["messages"] = list(snapshot["messages"])
        self.calls.append(snapshot)
        if self.raise_on_call:
            raise self.raise_on_call
        if not self.script:
            raise RuntimeError("fake anthropic: script exhausted, add more canned responses")
        return self.script.pop(0)


class Anthropic:
    def __init__(self, api_key=None, timeout=None):
        self.api_key = api_key
        self.timeout = timeout
        self.messages = _MessagesAPI()
