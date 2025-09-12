"""
API Routers for Parque Marino Backend v1
"""

from rest_framework.routers import DefaultRouter
from apps.business.wildlife.views import (
    ConservationStatusViewSet,
    SpecieViewSet,
    AnimalViewSet,
    HabitatViewSet
)

# Create a router and register our viewsets with it.
router = DefaultRouter()

# Wildlife routes
router.register(r'conservation-status', ConservationStatusViewSet)
router.register(r'species', SpecieViewSet)
router.register(r'animals', AnimalViewSet)
router.register(r'habitats', HabitatViewSet)

# Export the router URLs
urlpatterns = router.urls