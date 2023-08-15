from django.contrib import admin
from users.models import User, BlacklistedUsernames

admin.site.register(User)
admin.site.register(BlacklistedUsernames)
