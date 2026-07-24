"""eBay Marketplace Account Deletion / Closure notification endpoint.

GET  challenge -> {"challengeResponse": sha256(challengeCode + token + endpointUrl)}
POST notification -> 200. Python stdlib only. Vercel function at /api/ebay-deletion.
"""

import hashlib
import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

DEFAULT_TOKEN = "pAHDfJIqYTu8ri4Yz3T6Zx64vQaXNn4YFA8e4O6z8fKpgNNV"


def _verification_token():
    return os.environ.get("EBAY_VERIFICATION_TOKEN", DEFAULT_TOKEN)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        challenge = parse_qs(parsed.query).get("challenge_code", [""])[0]
        host = self.headers.get("X-Forwarded-Host") or self.headers.get("Host") or ""
        scheme = self.headers.get("X-Forwarded-Proto", "https")
        endpoint = scheme + "://" + host + parsed.path
        digest = hashlib.sha256(
            (challenge + _verification_token() + endpoint).encode("utf-8")
        ).hexdigest()
        body = json.dumps({"challengeResponse": digest}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length:
            self.rfile.read(length)
        self.send_response(200)
        self.end_headers()
