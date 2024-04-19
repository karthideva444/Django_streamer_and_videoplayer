from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MachineViewSet, ProductionLogViewSet

router = DefaultRouter()
router.register(r'machines', MachineViewSet)
router.register(r'production', ProductionLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]