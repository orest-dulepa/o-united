from entitlements.exceptions import ValidationError


class FeatureUnavailable(ValidationError):
    pass


class BrokenLicense(Exception):
    pass


class LicenseCorrupted(BrokenLicense):
    pass


class LicenseModelNotFound(Exception):
    pass
