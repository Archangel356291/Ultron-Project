"""Minimal fake of the 'discord' package — just enough surface area to
import and exercise bot.py's logic without a real Discord connection."""


class Embed:
    def __init__(self, title=None, description=None, color=None):
        self.title = title
        self.description = description
        self.color = color
        self.fields = []
        self.footer_text = None

    def add_field(self, name, value, inline=True):
        self.fields.append({"name": name, "value": value, "inline": inline})
        return self

    def set_footer(self, text):
        self.footer_text = text
        return self


class Intents:
    @staticmethod
    def default():
        return Intents()


class Object:
    def __init__(self, id):
        self.id = id


class User:
    def __init__(self, id):
        self.id = id


class HTTPException(Exception):
    pass


class File:
    """Fake discord.File — just captures what was passed so tests can
    assert on the actual bytes/filename sent, not merely that *a* file
    was attached."""
    def __init__(self, fp, filename=None):
        self.fp = fp
        self.filename = filename
        # read eagerly, like the real File does internally, so tests can
        # inspect content without needing to know about seek positions
        try:
            self.content_bytes = fp.read()
        except Exception:
            self.content_bytes = None


class ButtonStyle:
    primary = "primary"
    secondary = "secondary"
    success = "success"
    danger = "danger"
    link = "link"


class _MockMessage:
    """Fake discord.Message — tracks edits so tests can assert on them."""
    def __init__(self, content=None, embed=None, view=None):
        self.content = content
        self.embed = embed
        self.view = view
        self.file = None
        self.edits = []  # history of every edit call, for assertions

    async def edit(self, content=None, embed=None, view=None):
        # discord.py's real edit() only changes fields you pass; None means
        # "leave unchanged" for content/embed, but view=None legitimately
        # means "remove the view" if explicitly passed as a kwarg. Since our
        # test callers always pass what they mean, treat all three as
        # explicit-set-if-provided for simplicity of the fake.
        if content is not None:
            self.content = content
        if embed is not None:
            self.embed = embed
        if view is not None:
            self.view = view
        self.edits.append({"content": content, "embed": embed, "view": view})


class Interaction:
    """Fake interaction for testing command and button handlers directly."""
    def __init__(self, user_id):
        self.user = User(user_id)
        self.response = _InteractionResponse()
        self.followup = _Followup()


class _InteractionResponse:
    def __init__(self):
        self.sent = None
        self.deferred = False
        self.edited = None

    async def send_message(self, content=None, embed=None, ephemeral=False):
        self.sent = {"content": content, "embed": embed, "ephemeral": ephemeral}

    async def defer(self):
        self.deferred = True

    async def edit_message(self, content=None, embed=None, view=None):
        self.edited = {"content": content, "embed": embed, "view": view}


class _Followup:
    def __init__(self):
        self.sent = []

    async def send(self, content=None, embed=None, view=None, file=None):
        msg = _MockMessage(content=content, embed=embed, view=view)
        msg.file = file
        self.sent.append(msg)
        return msg


class ui:
    ButtonStyle = ButtonStyle

    class Button:
        def __init__(self, label=None, style=None, custom_id=None, disabled=False, url=None, emoji=None):
            self.label = label
            self.style = style
            self.custom_id = custom_id
            self.disabled = disabled

    @staticmethod
    def button(label=None, style=None, **kwargs):
        """Matches @discord.ui.button(...). The fake doesn't need the full
        component-registration machinery real discord.py has — tests call
        view.confirm(interaction, button) / view.cancel(...) directly, the
        same way command functions are called directly elsewhere in these
        tests, so this decorator only needs to tag metadata, not rewire
        dispatch."""
        def decorator(fn):
            fn.__discord_button_meta__ = {"label": label, "style": style}
            return fn
        return decorator

    class View:
        def __init__(self, *, timeout=180.0):
            self.timeout = timeout
            self._stopped = False
            self._disabled = False

        def disable_all_items(self):
            self._disabled = True

        def stop(self):
            self._stopped = True

        async def interaction_check(self, interaction):
            return True

        async def on_timeout(self):
            pass


class app_commands:
    @staticmethod
    def describe(**kwargs):
        def decorator(fn):
            return fn
        return decorator

    @staticmethod
    def choices(**kwargs):
        def decorator(fn):
            return fn
        return decorator

    class Choice:
        def __init__(self, name, value):
            self.name = name
            self.value = value

        def __class_getitem__(cls, item):
            # supports the `app_commands.Choice[str]` type-hint syntax
            # bot.py uses as a parameter annotation
            return cls

    class CommandTree:
        def __init__(self, client):
            self.client = client
            self.commands = {}

        def command(self, name, description=""):
            def decorator(fn):
                self.commands[name] = fn
                return fn
            return decorator

        def copy_global_to(self, guild):
            pass

        async def sync(self, guild=None):
            return []
