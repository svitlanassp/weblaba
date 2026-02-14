from rest_framework import serializers
from .models import Trip, Category, Place, ChecklistItem, Expense, Checklist

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class PlaceSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Place
        fields = [
            'id', 'trip', 'category', 'category_name', 'title',
            'description', 'address', 'link', 'notes',
            'visit_date', 'visit_time', 'cost', 'order'
        ]
        read_only_fields = ['id']

    def validate(self, data):
        trip = data.get('trip')
        visit_date = data.get('visit_date')

        if visit_date and trip:
            if visit_date < trip.start_date or visit_date > trip.end_date:
                raise serializers.ValidationError({
                    "visit_date": "Дата візиту повинна бути в межах дат подорожі."
                })
        return data

class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = ['id', 'checklist', 'text', 'is_done']
        read_only_fields = ['id']

class ChecklistSerializer(serializers.ModelSerializer):
    items = ChecklistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Checklist
        fields = ['id', 'trip', 'title', 'items']
        read_only_fields = ['id']


class TripListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Trip
        fields = ['id', 'user', 'title', 'country', 'city', 'start_date', 'end_date']

class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    date = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = ['id', 'trip', 'category', 'category_name', 'title', 'amount', 'date']
        read_only_fields = ['id']

    def get_date(self, obj):
        if obj.date and hasattr(obj.date, 'date'):
            return obj.date.date().isoformat()
        return obj.date.isoformat() if obj.date else None


class TripDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    places = PlaceSerializer(many=True, read_only=True)
    checklists = ChecklistSerializer(many=True, read_only=True)
    expenses = ExpenseSerializer(many=True, read_only=True)

    total_spent = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def get_total_spent(self, obj):
        places_cost = sum(place.cost for place in obj.places.all())
        additional_expenses = sum(exp.amount for exp in obj.expenses.all())
        return places_cost + additional_expenses

    def validate(self, data):
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError({"end_date": "Дата закінчення не може бути раніше початку."})
        return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Паролі не збігаються."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

