from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import *
from .repositories.manager import repo_manager


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class TripListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        trips = repo_manager.trips.get_user_trips(user=request.user)
        serializer = TripListSerializer(trips, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TripListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            new_trip = repo_manager.trips.create(**serializer.validated_data)

            return Response(TripListSerializer(new_trip).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TripDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        trip = repo_manager.trips.get_by_id(pk)

        if not trip or trip.user != request.user:
            return Response({"error": "Подорож не знайдена"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TripDetailSerializer(trip)
        return Response(serializer.data)

    def put(self, request, pk):
        trip = repo_manager.trips.get_by_id(pk)
        if not trip or trip.user != request.user:
            return Response({"error": "Подорож не знайдена"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TripDetailSerializer(trip, data=request.data, partial=True)
        if serializer.is_valid():
            updated_trip = repo_manager.trips.update(pk, **serializer.validated_data)
            return Response(TripDetailSerializer(updated_trip).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        trip = repo_manager.trips.get_by_id(pk)
        if not trip or trip.user != request.user:
            return Response({"error": "Подорож не знайдена"}, status=status.HTTP_404_NOT_FOUND)

        repo_manager.trips.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        categories = repo_manager.categories.get_all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ChecklistToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        item = repo_manager.checklist_items.toggle_item(pk)
        if not item or item.checklist.trip.user != request.user:
            return Response({"error": "Пункт не знайдено або доступ заборонено"}, status=status.HTTP_404_NOT_FOUND)

        return Response(ChecklistItemSerializer(item).data)


class PlaceDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        place = repo_manager.places.get_by_id(pk)
        if not place or place.trip.user != request.user:
            return Response({"error": "Місце не знайдено"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlaceSerializer(place)
        return Response(serializer.data)

    def put(self, request, pk):
        place = repo_manager.places.get_by_id(pk)
        if not place or place.trip.user != request.user:
            return Response({"error": "Об'єкт не знайдено"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlaceSerializer(place, data=request.data, partial=True)
        if serializer.is_valid():
            updated_place = repo_manager.places.update(pk, **serializer.validated_data)
            return Response(PlaceSerializer(updated_place).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        place = repo_manager.places.get_by_id(pk)
        if not place or place.trip.user != request.user:
            return Response({"error": "Об'єкт не знайдено"}, status=status.HTTP_404_NOT_FOUND)

        repo_manager.places.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        new_order = request.data.get('order')

        if 'visit_date' in request.data:
            new_date = request.data.get('visit_date')
        else:
            new_date = None

        success = repo_manager.places.update_dnd_status(pk, new_order, new_date)
        if success:
            return Response({"status": "updated"})
        return Response({"error": "failed"}, status=400)

class PlaceListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            trip = repo_manager.trips.get_by_id(request.data.get('trip'))
            if not trip or trip.user != request.user:
                return Response({"error": "Подорож не знайдена або не належить вам"},
                                status=status.HTTP_403_FORBIDDEN)

            new_place = repo_manager.places.create(**serializer.validated_data)
            return Response(PlaceSerializer(new_place).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChecklistGroupCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChecklistSerializer(data=request.data)
        if serializer.is_valid():
            trip = repo_manager.trips.get_by_id(request.data.get('trip'))
            if not trip or trip.user != request.user:
                return Response({"error": "Подорож не знайдена"}, status=status.HTTP_403_FORBIDDEN)

            new_group = repo_manager.checklists.create(**serializer.validated_data)
            return Response(ChecklistSerializer(new_group).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChecklistItemCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChecklistItemSerializer(data=request.data)
        if serializer.is_valid():
            group = repo_manager.checklists.get_by_id(request.data.get('checklist'))
            if not group or group.trip.user != request.user:
                return Response({"error": "Група чек-ліста не знайдена"}, status=status.HTTP_403_FORBIDDEN)

            new_item = repo_manager.checklist_items.create(**serializer.validated_data)
            return Response(ChecklistItemSerializer(new_item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            trip = repo_manager.trips.get_by_id(request.data.get('trip'))
            if not trip or trip.user != request.user:
                return Response({"error": "Подорож не знайдена"}, status=status.HTTP_403_FORBIDDEN)

            new_expense = repo_manager.expenses.create(**serializer.validated_data)
            return Response(ExpenseSerializer(new_expense).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        expense = repo_manager.expenses.get_by_id(pk)
        if not expense or expense.trip.user != request.user:
            return Response({"error": "Витрата не знайдена"}, status=status.HTTP_404_NOT_FOUND)

        repo_manager.expenses.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChecklistGroupDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        group = repo_manager.checklists.get_by_id(pk)
        if not group or group.trip.user != request.user:
            return Response({"error": "Група не знайдена"}, status=status.HTTP_404_NOT_FOUND)

        repo_manager.checklists.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChecklistItemDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        item = repo_manager.checklist_items.get_by_id(pk)
        if not item or item.checklist.trip.user != request.user:
            return Response({"error": "Пункт не знайдено"}, status=status.HTTP_404_NOT_FOUND)

        repo_manager.checklist_items.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)