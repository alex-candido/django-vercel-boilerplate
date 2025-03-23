from django.db.models import Count
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save()

class TaskReportView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(completed=True).count()
        pending_tasks = total_tasks - completed_tasks

        recent_tasks = tasks.order_by('-created_at')[:5]

        report = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'completion_rate': f"{(completed_tasks / total_tasks * 100) if total_tasks > 0 else 0:.1f}%",
            'recent_tasks': TaskSerializer(recent_tasks, many=True).data
        }

        return Response(report, status=status.HTTP_200_OK)