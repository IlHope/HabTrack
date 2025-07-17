from django.db import models
from django.contrib.auth.models import User     # встроенная модель пользователя

# Вспомогательный выбор повторяемости
PERIODICITY_CHOICES = [
    ('daily', 'Ежедневно'),
    ('weekly', 'Раз в неделю'),
    ('monthly', 'Раз в месяц'),
]

class Habit(models.Model):  # Привычка пользователя
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=100)
    periodicity = models.CharField(max_length=10, choices=PERIODICITY_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Goal(models.Model):   # Цель пользователя
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    target_value = models.PositiveIntegerField()    # Например, "прочитать 12 книг"
    current_value = models.PositiveIntegerField(default=0)  # Например, "уже прочитано 5"

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class HabitAction(models.Model):    # Отметка, что пользователь выполнил привычку в определенный день
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='actions')
    date = models.DateField()   # когда пользователь выполнил привычку

    def __str__(self):
        return f"{self.habit.name} - {self.date}"

class GoalProgress(models.Model):   # Пользователь обновил прогресс по цели, на сколько-то единиц
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='progress')
    date = models.DateField(auto_now_add=True)
    increment = models.PositiveIntegerField()   # на сколько продвинулся пользователь

    def __str__(self):
        return f"{self.goal.title} +{self.increment} on {self.date}"
