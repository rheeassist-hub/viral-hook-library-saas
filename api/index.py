import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import app  # noqa: E402

# Vercel Python runtime looks for `app` (ASGI) in this module.
