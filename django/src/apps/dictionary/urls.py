from django.urls import path, include

from rest_framework import routers

from apps.dictionary.views import (
    WordViewSet,
    DefinitionViewSet,
)

router = routers.DefaultRouter()
router.register("words", WordViewSet)
router.register("definitions", DefinitionViewSet)

urlpatterns = [path("api/", include(router.urls))]
