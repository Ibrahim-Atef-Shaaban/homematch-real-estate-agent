"""HomeMatch - script entry point.

The project is developed in HomeMatch.ipynb; this module exists for running
the same pipeline outside a notebook.

Credentials are read from the environment, never hardcoded. Copy .env.example
to .env and fill in your key (.env is gitignored).
"""

import os

from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("OPENAI_API_BASE", "https://api.openai.com/v1")

if not os.environ.get("OPENAI_API_KEY"):
    raise SystemExit("OPENAI_API_KEY is not set. See .env.example.")

from langchain.llms import OpenAI  # noqa: E402  (import after env setup)
