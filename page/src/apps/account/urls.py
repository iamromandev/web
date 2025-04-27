from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProfileCreateView, ProfileViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns: list = [
    # path('api/', include(router.urls)),
    path(
        'api/profiles/',
        ProfileCreateView.as_view(),
        name='profile-create',
    ),
]
