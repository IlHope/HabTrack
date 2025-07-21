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

    def create(self, validated_data):
        goal = validated_data["goal"]
        increment = validated_data["increment"]

        # Обновляем прогресс
        goal.current_value += increment

        # Проверяем завершена ли цель
        if goal.current_value >= goal.target_value:
            goal.current_value = goal.target_value  # ограничим сверху

        goal.save()

        # Создаём запись о прогрессе
        return GoalProgress.objects.create(**validated_data)
