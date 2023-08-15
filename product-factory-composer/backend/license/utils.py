import ast
import base64
import inspect
import hashlib
import re
import types
from functools import wraps
from django.conf import settings
from django.utils.module_loading import import_string, import_module

from license.exceptions import LicenseModelNotFound, FeatureUnavailable


def protect_f(f):
    source = inspect.getsource(f)
    indent = re.search(r"^(\s+)", source)
    if indent is not None:
        source = "\n".join([re.sub(r"^" + indent.group(1), "", line)
                            for line in source.split("\n")])

    code = compile(ast.parse(source), "<django>", 'exec')
    fn_code = None
    for item in code.co_consts:
        if isinstance(item, code.__class__):
            fn_code = item
            break
    return types.FunctionType(fn_code, f.__globals__, f.__name__,
                              f.__defaults__, f.__closure__)


def import_path(path):
    try:
        return import_string(path)
    except ImportError:
        pass

    try:
        return import_module(path)
    except ImportError:
        pass

    parts = path.rsplit('.', 1)
    if len(parts) > 1:
        return getattr(import_path(parts[0]), parts[1])

    raise ImportError


def checksum(path):
    code = inspect.getsource(import_path(path))
    return hashlib.sha256(code.encode()).hexdigest()


def is_base64(s):
    try:
        return base64.b64encode(base64.b64decode(s)) == s
    except Exception:
        return False


def process_checksums(paths):
    result = []
    for path in paths:
        if is_base64(path):
            path, _ = base64.b64decode(path).split(':', 1)
        result.append(base64.b64encode(":".join((path, checksum(path))).encode()))
    return result


def get_current_license():
    # the following dependencies should be loaded when the method called,
    # otherwise django apps won't load
    from django.apps import apps
    from entitlements.django import Model as EntitlementsModel

    license_cls = globals().get('_license_model')
    if license_cls is None:
        license_cls = None
        for model in apps.get_models():
            if issubclass(model, EntitlementsModel):
                license_cls = model
                break
        if license_cls is None:
            raise LicenseModelNotFound()

        globals()['_license_model'] = license_cls

    if license_cls is not None:
        return license_cls.get_current()

    return None


def valid_only(raise_exception=True, **properties):
    def wrapper(fn):
        @wraps(fn)
        def nested(*args, **kwargs):
            validate(raise_exception, **properties)
            return fn(*args, **kwargs)
        return nested
    return wrapper


def validate(raise_exception=True, **properties):
    if 'features' in properties:
        return not features_enabled(properties['features'], raise_exception)
    else:
        return True


def features_enabled(features, raise_exception=True):
    unavailable = set(features) - set(settings.FEATURES_AVAILABLE)
    if len(unavailable) > 0:
        if raise_exception:
            raise FeatureUnavailable("Please buy a license to see this page")
        return False
    return True


def is_developer_edition():
    return False if get_current_license() else True
