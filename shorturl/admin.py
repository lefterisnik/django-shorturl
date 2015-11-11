# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *


class ShortURLInfoAdminInline(admin.StackedInline):
    model = ShortURLInfo


class ShortURLAdmin(admin.ModelAdmin):
    inlines = [
        ShortURLInfoAdminInline,
    ]

admin.site.register(ShortURL, ShortURLAdmin)