from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    title = models.CharField(max_length=200)

    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.city}, {self.country})"

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Place(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='places')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=250, verbose_name="Назва місця")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")


    address = models.CharField(max_length=500, blank=True, verbose_name="Адреса")
    link = models.URLField(blank=True, verbose_name="Посилання")
    notes = models.TextField(blank=True, verbose_name="Нотатки")

    visit_date = models.DateField(null=True, blank=True, verbose_name="Дата візиту")
    visit_time = models.TimeField(null=True, blank=True, verbose_name="Час візиту")

    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Вартість")
    order = models.PositiveIntegerField(default=0, null=True, verbose_name="Порядок")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Expense(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=now, verbose_name="Дата витрати")

class Checklist(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='checklists')
    title = models.CharField(max_length=200)

class ChecklistItem(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='items')
    text = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)
