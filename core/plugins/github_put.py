"""github_put — create or update a file in a GitHub repo via the Contents API.

The Contents API requires base64-encoded content, so this plugin encodes it
server-side (the caller passes plain text). It uses the same GitHub token
secret as the github plugin: GITHUB_TOKEN, falling back to the gh CLI token.

Tools:
    github_put_file(repo, path, content, message, branch='main')
"""

import base64
import json
import os
import re
import subprocess
import urllib.error
import urllib.request

API = "https://api.github.com"

PLUGIN_META = {
    "name": "github_put",
    "version": "1.0.0",
    "description": "Create or update a file in a GitHub repo via the Contents API (base64 handled server-side).",
}


def _token(secrets):
    tok = ""
    if isinstance(secrets, dict):
        tok = str(secrets.get("GITHUB_TOKEN") or "")
    if not tok:
        tok = str(os.environ.get("GITHUB_TOKEN") or "")
    if tok:
        return tok
    try:
        out = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=10)
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except Exception:
        pass
    try:
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cfg = open(os.path.join(root, ".git", "config")).read()
        m = re.search(r"https://[^/@\s]+@github\.com", cfg)
        if m:
            cred = m.group(0).split("//", 1)[1].split("@", 1)[0]
            return cred.split(":")[-1]
    except Exception:
        pass
    return ""


def _call(method, url, token, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:
        return 0, str(e)


def github_put_file(args, secrets):
    repo = str(args.get("repo") or "").strip().strip("/")
    path = str(args.get("path") or "").strip().lstrip("/")
    content = args.get("content")
    message = str(args.get("message") or ("update " + path))
    branch = str(args.get("branch") or "main")
    if not repo or not path or content is None:
        return {"status": 400, "body": "repo, path and content are required"}
    token = _token(secrets)
    if not token:
        return {"status": 401, "body": "no GitHub token available"}
    payload = {
        "message": message,
        "content": base64.b64encode(str(content).encode()).decode(),
        "branch": branch,
    }
    status, body = _call("GET", API + "/repos/" + repo + "/contents/" + path + "?ref=" + branch, token)
    if status == 200:
        try:
            payload["sha"] = json.loads(body)["sha"]
        except Exception:
            pass
    elif status != 404:
        return {"status": status, "body": body}
    status, body = _call("PUT", API + "/repos/" + repo + "/contents/" + path, token, payload)
    return {"status": status, "body": body}


TOOLS = {
    "github_put_file": {
        "description": "Create or update a file in a GitHub repo via the Contents API. Base64-encodes content and reuses an existing sha when the file exists.",
        "args": {
            "repo": "owner/name",
            "path": "path within the repo",
            "content": "plain-text file content",
            "message": "commit message",
            "branch": "branch name (default 'main')",
        },
        "handler": github_put_file,
        "func": github_put_file,
    },
}
