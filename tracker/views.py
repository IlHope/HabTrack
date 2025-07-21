from rest_framework import  viewsets
from .models import Habit, Goal, HabitAction, GoalProgress
from .serializers import HabitSerializer, GoalSerializer, HabitActionSerializer, GoalProgressSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def get_goal_progress(self, request, *args, **kwargs):
        goal = self.get_object()
        goal_progress = goal.progress.all().order_by("date")

        cumulative = 0
        result = {}

        for progress in goal_progress:
            cumulative += progress.increment
            result[str(progress.date)] = cumulative

        return Response(result)

class HabitActionViewSet(viewsets.ModelViewSet):
    queryset = HabitAction.objects.all()
    serializer_class = HabitActionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GoalProgressViewSet(viewsets.ModelViewSet):
    queryset = GoalProgress.objects.all()
    serializer_class = GoalProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
