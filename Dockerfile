# A working image with no HEALTHCHECK, and logs written to a file inside the container.
FROM python:3.12-slim

COPY app/ /srv/app/
WORKDIR /srv

EXPOSE 8080
CMD ["python3", "app/server.py"]
