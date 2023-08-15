from functools import wraps, partial
from threading import current_thread
from weakref import WeakKeyDictionary

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest
from entitlements.exceptions import ValidationError

from license.exceptions import LicenseModelNotFound
from license.loader import Loader, Context
from license.utils import get_current_license, protect_f, is_developer_edition

_contexts = WeakKeyDictionary()
empty = object()


def _get_active_context(request=None):
    return _contexts.get(current_thread()) or {}


@protect_f
def process_validation(self, raise_exception=True, **properties):
    outer = self._fn(raise_exception, **properties) if self is not None else True

    inner = outer is not False
    if inner is True:
        inner = validate(raise_exception, **properties)
    if not inner:
        ctx = _get_active_context()
        lic = ctx.get('license')
        if lic:
            lic.__dict__['is_valid'] = False

    return outer


class ValidationLoader:
    _fn = None

    def apply(self, obj, method):
        self._fn = getattr(obj, method)
        wrapped = partial(process_validation, self=self)
        setattr(obj, method, wraps(self._fn)(wrapped))
        return self


class ValidationResponseForException(Loader):
    def process(self, request, exc):
        if isinstance(exc, ValidationError):
            response = HttpResponseBadRequest("license error")
            # Force a TemplateResponse to be rendered.
            if (not getattr(response, 'is_rendered', True)
                    and callable(getattr(response, 'render', None))):
                response = response.render()
            return response
        return super().process(request, exc)


class LicenseRequestContext(Context):
    def context(self, request):
        process_validation(None, raise_exception=False)
        return (yield request)


class ValidationContext(Context):
    def __init__(self):
        super().__init__()
        self._ctx_patched = False

    def patch_context_processors(self):
        if self._ctx_patched:
            return

        for tmpl_conf in getattr(settings, 'TEMPLATES', []):
            cp = tmpl_conf.get('OPTIONS', {}).get('context_processors')
            if cp is not None:
                cp = list(cp)
                cp.append(".".join((_get_active_context.__module__,
                                    _get_active_context.__name__)))
                tmpl_conf['OPTIONS']['context_processors'] = cp
        self._ctx_patched = True

    def context(self, request):
        cur_thread = current_thread()
        self.patch_context_processors()

        ctx = {}
        try:
            ctx['license'] = get_current_license()
            request.license = ctx['license']
        except LicenseModelNotFound:
            pass
        _contexts.setdefault(current_thread(), ctx)

        try:
            response = yield request
        except ValidationError:
            response = HttpResponseBadRequest("license error")
        finally:
            if cur_thread in _contexts:
                del _contexts[cur_thread]

        return response


@protect_f
def validate(raise_exception=True, **properties):
    ctx = _get_active_context()
    if 'license' not in ctx:
        return True

    lic = ctx.get('license')
    try:
        if lic is None:
            raise ValidationError("No active license")

        lic.load_data()
        if lic.is_valid:
            validate_users(lic, **properties)
            validate_features(lic, **properties)
        else:
            raise ValidationError("Invalid license")
    except ValidationError as e:
        if not raise_exception:
            return ValidationError(e)
        raise

    return True


@protect_f
def validate_users(lic, **properties):
    user_model = get_user_model()
    user_limit = lic.get_property('user_limit', empty)
    if (user_limit is empty or
            (user_limit is not None and user_model.objects.count() > user_limit)):
        raise ValidationError("Users limit is exceeded")


@protect_f
def validate_features(lic, **properties):
    features = lic.get_property('features', empty)
    if features is empty or 'features' not in properties:
        return

    extras = set(properties['features']) - set(features or [])
    if extras:
        raise ValidationError("Features are unavailable: {}".format(", ".join(extras)))


def validate_development_edition(object_type):
    if object_type == "person":
        return check_valid_development_edition("talent", "Person", 5)
    elif object_type == "user":
        return check_valid_development_edition("auth", "User", 5)
    elif object_type == "product":
        return check_valid_development_edition("work", "Product", 2)


def check_valid_development_edition(app_name, model_name, object_count):
    if not is_developer_edition():
        return True

    searched_model = apps.get_model(app_name, model_name)
    if not searched_model:
        return False

    if searched_model.objects.count() >= object_count:
        if object_count > 1:
            model_name += "s"
        raise ValidationError(f"The application is in the development version. Please upgrade your license to "
                              f"create more than {object_count} {model_name.lower()}.")

    return True
