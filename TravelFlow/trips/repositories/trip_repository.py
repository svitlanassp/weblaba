from .base_repository import BaseRepository
from trips.models import Trip

class TripRepository(BaseRepository):
    def __init__(self):
        super().__init__(Trip)

    def get_user_trips(self, user):
        return self.model.objects.filter(user=user).order_by('-created_at')