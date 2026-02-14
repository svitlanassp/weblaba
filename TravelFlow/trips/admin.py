from django.contrib import admin
from .models import Trip, Category, Place, ChecklistItem

# Реєструємо моделі, щоб вони з'явилися в інтерфейсі
admin.site.register(Trip)
admin.site.register(Category)
admin.site.register(Place)
admin.site.register(ChecklistItem)