from django.contrib import admin
from django.contrib.auth.models import Group
from .models import ScholarshipApplication

admin.site.register(ScholarshipApplication)

admin.site.unregister(Group)