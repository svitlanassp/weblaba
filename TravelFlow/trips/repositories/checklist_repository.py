from .base_repository import BaseRepository
from trips.models import Checklist, ChecklistItem

class ChecklistGroupRepository(BaseRepository):
    def __init__(self):
        super().__init__(Checklist)

    def get_by_trip(self, trip_id):
        return self.model.objects.filter(trip_id=trip_id)

class ChecklistItemRepository(BaseRepository):
    def __init__(self):
        super().__init__(ChecklistItem)

    def get_by_group(self, checklist_id):
        return self.model.objects.filter(checklist_id=checklist_id)

    def toggle_item(self, item_id):
        item = self.get_by_id(item_id)
        if item:
            item.is_done = not item.is_done
            item.save()
        return item