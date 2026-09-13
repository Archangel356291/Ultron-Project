"""A real MCP server for testing app.py's MCP client against genuine
JSON-RPC traffic, not a hand-rolled mock. Implements the protocol shapes
verified via research: initialize -> notifications/initialized handshake
with an Mcp-Session-Id response header, tools/list, and tools/call with
content/isError. Strict about request shape — rejects anything that
doesn't look like the real spec, so a bug in the client's requests would
be caught here, not hidden by a lenient mock."""
import json
import sys
import uuid
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

REQUIRED_AUTH_TOKEN = sys.argv[1] if len(sys.argv) > 1 else None
SESSIONS = {}

TOOLS = [
    {
        "name": "echo",
        "description": "Echoes back whatever text you send it.",
        "inputSchema": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    },
    {
        "name": "fail_on_purpose",
        "description": "Always returns a tool-level error (isError: true), for testing error handling.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "huge_response",
        "description": "Returns a very long response, for testing truncation.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "not_approved_tool",
        "description": "A real tool that exists but is never in any test's auto_approve list.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def jsonrpc_result(req_id, result):
    return jsonify({"jsonrpc": "2.0", "id": req_id, "result": result})


def jsonrpc_error(req_id, code, message):
    return jsonify({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}})


@app.route("/mcp", methods=["POST"])
def mcp_endpoint():
    if REQUIRED_AUTH_TOKEN:
        auth = request.headers.get("Authorization", "")
        if auth != f"Bearer {REQUIRED_AUTH_TOKEN}":
            return Response(
                json.dumps({"jsonrpc": "2.0", "error": {"code": -32001, "message": "unauthorized"}}),
                status=401, mimetype="application/json",
            )

    body = request.get_json(force=True, silent=True) or {}
    assert body.get("jsonrpc") == "2.0", f"malformed request, missing jsonrpc 2.0: {body}"
    method = body.get("method")
    req_id = body.get("id")
    params = body.get("params") or {}
    is_notification = "id" not in body

    if method == "initialize":
        assert "protocolVersion" in params, f"initialize missing protocolVersion: {params}"
        session_id = str(uuid.uuid4())
        SESSIONS[session_id] = True
        resp = jsonrpc_result(req_id, {
            "protocolVersion": params["protocolVersion"],
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "test-mcp-server", "version": "1.0"},
        })
        resp.headers["Mcp-Session-Id"] = session_id
        return resp

    if method == "notifications/initialized":
        assert is_notification, "notifications/initialized must be sent without an id"
        return ("", 202)

    session_id = request.headers.get("Mcp-Session-Id")
    assert session_id in SESSIONS, f"tools/* called without a valid Mcp-Session-Id (got {session_id!r})"

    if method == "tools/list":
        return jsonrpc_result(req_id, {"tools": TOOLS})

    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments", {})
        assert "name" in params, f"tools/call missing 'name': {params}"

        if name == "echo":
            return jsonrpc_result(req_id, {
                "content": [{"type": "text", "text": f"you said: {arguments.get('text', '')}"}],
                "isError": False,
            })
        if name == "fail_on_purpose":
            return jsonrpc_result(req_id, {
                "content": [{"type": "text", "text": "this tool always fails, on purpose"}],
                "isError": True,
            })
        if name == "huge_response":
            return jsonrpc_result(req_id, {
                "content": [{"type": "text", "text": "x" * 50000}],
                "isError": False,
            })
        if name == "not_approved_tool":
            return jsonrpc_result(req_id, {
                "content": [{"type": "text", "text": "you should never see this — this tool should never be called"}],
                "isError": False,
            })
        return jsonrpc_error(req_id, -32601, f"unknown tool: {name}")

    return jsonrpc_error(req_id, -32601, f"unknown method: {method}")


if __name__ == "__main__":
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 6001
    app.run(host="127.0.0.1", port=port)
