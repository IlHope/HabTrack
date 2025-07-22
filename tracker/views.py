from rest_framework import  viewsets
from .models import Habit, Goal, HabitAction, GoalProgress
from .serializers import HabitSerializer, GoalSerializer, HabitActionSerializer, GoalProgressSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date, timedelta

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def reminders(self, request):
        today = date.today()
        habits = self.get_queryset().filter(is_active=True)
        missed = []

        for habit in habits:
            last_action = habit.actions.order_by('-date').first()

            if habit.periodicity == 'daily':
                should_do = True

            elif habit.periodicity == 'weekly':
                should_do = (not last_action or (today - last_action.date).days >= 7)

            elif habit.periodicity == 'monthly':
                should_do = (not last_action or (today - last_action.date).days >= 30)

            else:
                should_do = False

            if should_do and not habits.actions.filter(date=today).exists():
                missed.append(habit)

        serializer = self.get_serializer(missed, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def calendar(self, request):
        habit = self.get_object()
        dates = habit.actions.values_list('date', flat=True).order_by('date')

        return Response(dates)

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
