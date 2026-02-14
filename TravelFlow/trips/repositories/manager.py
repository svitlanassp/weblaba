from .expense_repository import ExpenseRepository
from .trip_repository import TripRepository
from .place_repository import PlaceRepository
from .category_repository import CategoryRepository
from .checklist_repository import ChecklistGroupRepository, ChecklistItemRepository


class RepositoryManager:
    def __init__(self):
        self.trips = TripRepository()
        self.places = PlaceRepository()
        self.categories = CategoryRepository()
        self.expenses = ExpenseRepository()
        self.checklists = ChecklistGroupRepository()
        self.checklist_items = ChecklistItemRepository()

repo_manager = RepositoryManager()