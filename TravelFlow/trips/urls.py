from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),

    path('trips/', TripListCreateView.as_view(), name='trip_list'),
    path('trips/<int:pk>/', TripDetailView.as_view(), name='trip_detail'),
    path('places/', PlaceListCreateView.as_view(), name='place_create'),
    path('places/<int:pk>/', PlaceDetailView.as_view(), name='place_detail'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('expenses/', ExpenseListCreateView.as_view(), name='expense_create'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense_delete'),

    path('checklists/groups/', ChecklistGroupCreateView.as_view(), name='checklist_group_create'),
    path('checklists/groups/<int:pk>/', ChecklistGroupDetailView.as_view(), name='checklist_group_detail'),

    path('checklists/items/', ChecklistItemCreateView.as_view(), name='checklist_item_create'),
    path('checklists/items/<int:pk>/', ChecklistItemDetailView.as_view(), name='checklist_item_detail'),
    path('checklists/items/<int:pk>/toggle/', ChecklistToggleView.as_view(), name='checklist_toggle'),

]