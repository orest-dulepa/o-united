from collections import deque
from functools import wraps
from threading import current_thread
from weakref import WeakKeyDictionary
from uuid import uuid4

from django.http.response import HttpResponse


class Loader:
    _fn = None

    def apply(self, obj, method):
        self._fn = getattr(obj, method)

        @wraps(self._fn)
        def wrapper(*args, **kwargs):
            return self.process(*args, **kwargs)

        setattr(obj, method, wrapper)
        return self

    def process(self, *args, **kwargs):
        return self._fn(*args, **kwargs)


class RequestLoader(Loader):
    def __init__(self, *request_ctx, protected_regexp=None, excluded_regexp=None):
        self._excluded_regexp = excluded_regexp
        self._protected_regexp = protected_regexp
        self._request_ctx = request_ctx

    def process(self, handler, request):
        if self.is_protected(request):
            stack = [ctx.context(request) for ctx in self._request_ctx]
            for ctx in stack:
                request = next(ctx)
            response = super(RequestLoader, self).process(handler, request)
            for ctx in stack[::-1]:
                try:
                    ctx.send(response)
                except StopIteration as e:
                    if e.value is not None:
                        response = e.value

            return response

    def is_protected(self, request):
        result = self._protected_regexp is None
        for regexp in self._protected_regexp or []:
            if regexp.match(request.path):
                result = True
                break
        if result:
            for regexp in self._excluded_regexp or []:
                if regexp.match(request.path):
                    result = False
                    break
        return result


class Context:
    def context(self, *args, **kwargs):
        raise NotImplementedError


class SkippedContext(Context):
    class CheckPoint:
        def __init__(self):
            self.uid = uuid4()
            self.called = 0

        def increment(self):
            self.called += 1

        def __bool__(self):
            return bool(self.called)

    def __init__(self):
        self._contexts = WeakKeyDictionary()

    def context(self, request):
        q = self._contexts.setdefault(current_thread(), deque())
        q.appendleft(self.CheckPoint())

        response = yield request

        cp = q.popleft()
        if not cp:
            response = self.on_skipped(response)
        return response

    def _active_checkpoint(self):
        q = self._contexts.setdefault(current_thread(), deque())
        if len(q):
            return q[0]
        return None

    def set_processed(self):
        cp = self._active_checkpoint()
        if cp is not None:
            cp.increment()

    def on_skipped(self, response):
        return response


class SkippedContextLoader(SkippedContext, Loader):
    def process(self, obj, *args, **kwargs):
        try:
            return super(SkippedContextLoader, self).process(obj, *args, **kwargs)
        finally:
            self.set_processed()


class DeniedContextLoader(SkippedContextLoader):
    def on_skipped(self, response):
        return HttpResponse(status=400)
