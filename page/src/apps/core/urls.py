from django.urls import path

from .views import SelfUserRetrieveView

urlpatterns = [
    path('users/self/', SelfUserRetrieveView.as_view(), name='self-user-retrieve'),
]
