from __future__ import annotations

from typing import Iterable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.security.auth import constant_time_equals, get_auth_config


class ApiTokenMiddleware(BaseHTTPMiddleware):
    """
    If JARVIS_REQUIRE_AUTH=true and JARVIS_API_TOKEN is set,
    requests to protected paths must include header: X-API-Token: <token>.
    """

    def __init__(self, app, *, protected_prefixes: Iterable[str]) -> None:
        super().__init__(app)
        self.protected_prefixes = tuple(protected_prefixes)

    async def dispatch(self, request: Request, call_next) -> Response:
        cfg = get_auth_config()
        if not cfg.require_auth or not cfg.api_token:
            return await call_next(request)

        path = request.url.path or ""
        if not any(path.startswith(p) for p in self.protected_prefixes):
            return await call_next(request)

        token = request.headers.get("x-api-token", "")
        if not constant_time_equals(token, cfg.api_token):
            return JSONResponse({"detail": "Unauthorized"}, status_code=401)

        return await call_next(request)

