from rest_framework import  viewsets
from .models import Habit, Goal, HabitAction, GoalProgress
from .serializers import HabitSerializer, GoalSerializer, HabitActionSerializer, GoalProgressSerializer

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

class HabitActionViewSet(viewsets.ModelViewSet):
    queryset = HabitAction.objects.all()
    serializer_class = HabitActionSerializer

class GoalProgressViewSet(viewsets.ModelViewSet):
    queryset = GoalProgress.objects.all()
    serializer_class = GoalSerializer
