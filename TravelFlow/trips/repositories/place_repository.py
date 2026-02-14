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

    def update_dnd_status(self, place_id, new_order=None, new_date=None):
        update_data = {}

        if new_order is not None:
            update_data['order'] = new_order

        update_data['visit_date'] = new_date if new_date != "" else None

        return self.update(place_id, **update_data)