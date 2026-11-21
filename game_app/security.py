"""Form security helpers shared by authentication and game routes."""

import hmac
import secrets

from flask import abort, session


def csrf_token() -> str:
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token


def validate_csrf(submitted_token: str) -> None:
    expected_token = session.get("csrf_token", "")
    if (
        not submitted_token
        or not expected_token
        or not hmac.compare_digest(submitted_token, expected_token)
    ):
        abort(400, description="A sessão do formulário expirou. Atualize a página e tente novamente.")
