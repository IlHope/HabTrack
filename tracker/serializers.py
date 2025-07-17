from rest_framework import serializers
from .models import Habit, Goal, HabitAction, GoalProgress

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'

class HabitActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitAction
        fields = '__all__'

class GoalProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalProgress
        fields = '__all__'