from django.contrib import admin

from .models import Trip, Category, Place, ChecklistItem, Expense

admin.site.register(Trip)
admin.site.register(Category)
admin.site.register(Place)
admin.site.register(ChecklistItem)
admin.site.register(Expense)