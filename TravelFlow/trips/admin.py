from django.contrib import admin

from .models import Trip, Place, ChecklistItem, Expense

admin.site.register(Trip)
admin.site.register(Place)
admin.site.register(ChecklistItem)
admin.site.register(Expense)