"""Self-check for the /api/tts streaming fix (Module 1 of the roadmap:
"text appears immediately, audio lags proportional to message length").

The bug was buffering on both ends: _fish_audio_tts used to call
resp.read() and wait for Fish Audio's ENTIRE reply before returning,
even though Fish Audio's own /v1/tts already streams via chunked
transfer. The fix makes _fish_audio_tts return a chunk generator instead
of pre-read bytes, and the /api/tts route forward those chunks via
Flask's stream_with_context instead of buffering into one Response body.

This proves the observable contract that actually matters: chunks reach
the HTTP layer as they're produced, not only after the last one exists —
by monkeypatching _fish_audio_tts with a generator that only yields its
second chunk after an explicit signal, then asserting the Flask dev
server has already sent the first chunk to a real socket before that
signal fires. A non-streaming implementation (Response(b"".join(...)))
would fail this: it can't send anything until the whole generator is
exhausted, so the first chunk would never arrive before the signal.

Run standalone from anywhere:
    python dev-tools/test_tts_streaming.py
"""
import os
import socket
import sys
import tempfile
import threading
import time

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "odin-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)
sys.path.insert(0, BACKEND_DIR)

os.environ["ODIN_API_TOKEN"] = "admin-test-token"
os.environ["ODIN_FISH_AUDIO_API_KEY"] = "fake-fish-key"
os.environ["ODIN_FISH_VOICE_ID"] = "fake-voice-id"
os.environ["ODIN_DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test_odin.db")
os.environ["ODIN_DISABLE_MEMORY_TRENDS"] = "1"

import app  # noqa: E402

FIRST_CHUNK = b"\xff\xfb" + b"1" * 4000   # oversized so it can't hide in a TCP/OS buffer unnoticed
SECOND_CHUNK = b"2" * 4000
release_second_chunk = threading.Event()


def _fake_streaming_tts(text):
    def _chunks():
        yield FIRST_CHUNK
        release_second_chunk.wait(timeout=5)   # only yields chunk 2 once the test says so
        yield SECOND_CHUNK
    return _chunks(), "audio/mpeg", None


def demo():
    app._fish_audio_tts = _fake_streaming_tts

    # Run the real Flask app (not the test client — the test client buffers
    # the whole response before returning it, which would hide exactly the
    # bug being tested for) on a real socket, in a background thread.
    import werkzeug.serving
    server = werkzeug.serving.make_server("127.0.0.1", 0, app.app)
    port = server.server_port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        sock = socket.create_connection(("127.0.0.1", port), timeout=5)
        try:
            req = (
                b"POST /api/tts HTTP/1.1\r\n"
                b"Host: 127.0.0.1\r\n"
                b"Authorization: Bearer admin-test-token\r\n"
                b"Content-Type: application/json\r\n"
                b"Content-Length: 20\r\n"
                b"Connection: close\r\n"
                b"\r\n"
                b'{"text": "hi there"}'
            )
            sock.sendall(req)

            # Read until the first chunk's own bytes have actually arrived,
            # or time out -- proves the server sent it before releasing the
            # second chunk, i.e. it streamed rather than buffered.
            received = b""
            deadline = time.time() + 5
            while FIRST_CHUNK not in received and time.time() < deadline:
                sock.settimeout(max(0.1, deadline - time.time()))
                try:
                    part = sock.recv(65536)
                except socket.timeout:
                    break
                if not part:
                    break
                received += part
            assert FIRST_CHUNK in received, (
                "first chunk never arrived on the socket before the second chunk "
                "was even released -- streaming is broken (back to full buffering)"
            )
            assert SECOND_CHUNK not in received, (
                "second chunk arrived before it was released -- test setup issue, "
                "not proving anything about streaming"
            )

            # Now let the rest through and confirm the full reply is still correct.
            release_second_chunk.set()
            deadline = time.time() + 5
            while SECOND_CHUNK not in received and time.time() < deadline:
                sock.settimeout(max(0.1, deadline - time.time()))
                try:
                    part = sock.recv(65536)
                except socket.timeout:
                    break
                if not part:
                    break
                received += part
            assert SECOND_CHUNK in received, "second chunk never arrived after being released"
        finally:
            sock.close()
    finally:
        server.shutdown()
        thread.join(timeout=5)

    print("OK: /api/tts streams the first chunk to the client before the rest of the "
          "reply exists, instead of buffering the whole reply first.")


if __name__ == "__main__":
    demo()
