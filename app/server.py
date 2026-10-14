"""Ola driver-location service.

The /health endpoint here returns 200 unconditionally, which is exactly as useless as having
no endpoint at all. Making it mean something is your work.
"""
import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", "8080"))
LOG_PATH = os.environ.get("LOG_PATH", "/var/log/app.log")

# The upstream driver feed. Set FEED_DOWN=1 to simulate it being unreachable — see the README.
FEED_DOWN = os.environ.get("FEED_DOWN", "") == "1"
STARTED = time.time()


def log(line):
    """Writes to a file inside the container, which is where logs go to die."""
    try:
        with open(LOG_PATH, "a") as fh:
            fh.write(line + "\n")
    except OSError:
        # Falls back to stdout when the path is not writable, which is how you are reading
        # anything at all when you run this outside a container.
        print(line, flush=True)


def feed_ok():
    return not FEED_DOWN


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        log(f"{self.command} {self.path}")
        if self.path == "/health":
            # TODO(you): this says 200 even when the feed is down.
            body, code = json.dumps({"status": "ok"}).encode(), 200
        elif self.path.startswith("/location"):
            if feed_ok():
                body = json.dumps({"driver_id": 4412, "lat": 12.9716, "lng": 77.5946}).encode()
                code = 200
            else:
                body, code = json.dumps({"error": "feed unavailable"}).encode(), 503
        else:
            body, code = json.dumps({"error": "not found"}).encode(), 404
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"ola driver-location listening on {PORT}, feed_down={FEED_DOWN}", flush=True)
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
