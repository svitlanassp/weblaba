from .base_repository import BaseRepository
from trips.models import Expense

class ExpenseRepository(BaseRepository):
    def __init__(self):
        super().__init__(Expense)

    def get_by_trip(self, trip_id):
        return self.model.objects.filter(trip_id=trip_id).order_by('-date')