from __future__ import annotations

from asgiref.local import Local

_state = Local()


class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _state.request = request
        return self.get_response(request)


def get_current_request():
    return getattr(_state, "request", None)

