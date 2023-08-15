from entitlements.django import Model
from django.conf import settings
from django.db import models


class LicenseManager(models.Manager):
    def current(self):
        return self.get_queryset().filter(current=True)\
            .order_by("-pk").first()


class License(Model):
    current = models.BooleanField(default=False, db_index=True)

    objects = LicenseManager()

    @classmethod
    def get_current(cls):
        return cls.objects.current()

    def get_property(self, key, default=None):
        product_data = self.properties.get(settings.LICENSE_PRODUCT)
        if product_data is not None:
            return product_data.get(key, default)
        return default

    def save(self, *args, **kwargs):
        if not self.pk and self.current:
            self.__class__.objects.filter(current=True).update(current=False)
        super().save(*args, **kwargs)


class ContributorAgreement(models.Model):
    product = models.ForeignKey(to="work.Product", on_delete=models.CASCADE)
    agreement_content = models.TextField()

    class Meta:
        db_table = "license_contributor_agreement"


class ContributorAgreementAcceptance(models.Model):
    agreement = models.ForeignKey(to=ContributorAgreement, on_delete=models.CASCADE)
    person = models.ForeignKey(to='talent.Person', on_delete=models.CASCADE)
    accepted_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "license_contributor_agreement_acceptance"


class ContributorGuide(models.Model):
    product = models.ForeignKey(to="work.Product", on_delete=models.CASCADE)
    title = models.CharField(max_length=60, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
