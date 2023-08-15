from graphene_django import DjangoObjectType
from license.models import ContributorAgreement, ContributorGuide


class LicenseType(DjangoObjectType):
    class Meta:
        model = ContributorAgreement


class ContributorGuideType(DjangoObjectType):
    class Meta:
        model = ContributorGuide
