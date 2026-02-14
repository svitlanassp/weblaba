from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('trips.urls')),
]