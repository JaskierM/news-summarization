import os
import sys

from enum import StrEnum


class Environment(StrEnum):
    dev = "dev"
    prod = "prod"


def detect_environment() -> Environment:
    explicit = os.getenv("APP_ENV")

    if explicit in (Environment.dev, Environment.prod):
        return Environment(explicit)

    try:
        if getattr(sys, "frozen", False) or hasattr(sys, "_MEIPASS"):
            return Environment.prod

        if os.getenv("KUBERNETES_SERVICE_HOST"):
            return Environment.prod

        if os.getenv("GUNICORN_CMD_ARGS") or os.getenv("SYSTEMD_EXEC_PID"):
            return Environment.prod

        if os.getenv("APP_DEPLOYED") == "1":
            return Environment.prod
    except Exception:
        pass

    return Environment.dev
