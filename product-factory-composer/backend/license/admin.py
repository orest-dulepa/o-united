from django.contrib import admin
from license.models import ContributorGuide, ContributorAgreement, ContributorAgreementAcceptance, License

admin.site.register(ContributorGuide)
admin.site.register(ContributorAgreement)
admin.site.register(ContributorAgreementAcceptance)
admin.site.register(License)
