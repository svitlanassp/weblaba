from .base_repository import BaseRepository
from trips.models import Place

class PlaceRepository(BaseRepository):
    def __init__(self):
        super().__init__(Place)

    def get_by_trip(self, trip_id):
        return self.model.objects.filter(trip_id=trip_id)

    def get_ideas_bank(self, trip_id):
        return self.model.objects.filter(trip_id=trip_id, visit_date__isnull=True)

    def get_calendar_places(self, trip_id):
        return self.model.objects.filter(trip_id=trip_id, visit_date__isnull=False)
