from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TaskReportView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]