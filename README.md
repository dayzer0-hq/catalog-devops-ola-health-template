# Ola driver-location service — a health check that can actually fail

`GET /location` returns a driver position. `GET /health` returns 200 **always**, even when the
service cannot do its job. That is the thing to fix.

## How to simulate the feed being down

    FEED_DOWN=1 python3 app/server.py

With the feed down, `/location` answers 503 and `/health` still answers 200. That gap is the
whole point of your first ticket.

## Where the logs currently go

`/var/log/app.log` **inside the container** — so `docker logs` shows nothing, and the file
disappears with the container. Outside a container the service falls back to stdout so you can
see anything at all.

## Run it

    python3 app/server.py
    curl localhost:8080/health
    curl localhost:8080/location
