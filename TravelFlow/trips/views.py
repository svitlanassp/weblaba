from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import *
from .repositories.manager import repo_manager
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer

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

class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        is_staff = data.get('is_staff', False)

        if not username or not password:
            return Response({"error": "Username та password обов'язкові."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                is_staff=is_staff
            )
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "Користувач з таким ім'ям вже існує."}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "Користувача не знайдено"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "Користувача не знайдено"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "Користувача не знайдено"}, status=status.HTTP_404_NOT_FOUND)

        if user == request.user:
            return Response({"error": "Ви не можете видалити самі себе"}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)