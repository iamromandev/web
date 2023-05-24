from django.urls import path
from apps.dashboard.views import dictionary_details

urlpatterns = [
    path('api/dictionary/', dictionary_details, name='dictionary-details'),
]
