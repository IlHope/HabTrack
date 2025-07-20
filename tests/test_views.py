import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from tracker.models import Habit, Goal
from datetime import date, timedelta

# Возвращение списка привычек
@pytest.mark.django_db
def test_habit_list_authenticated():
    user = User.objects.create_user(username="testuser", password="pass")
    Habit.objects.create(name="Test Habit", user=user)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/habits/")
    assert response.status_code == 200
    assert response.data[0]["name"] == "Test Habit"

# Доступ без авторизации
@pytest.mark.django_db
def test_habit_list_unauthenticated():
    client = APIClient()
    response = client.get("/api/habits/")
    assert response.status_code == 401

# Создание привычки
@pytest.mark.django_db
def test_create_habit():
    user = User.objects.create_user(username="testuser", password="pass")
    client = APIClient()
    client.force_authenticate(user=user)

    data = {
        "name": "New Habit",
        "periodicity": "daily",
        "is_active": True,
        "user": user.id
    }
    response = client.post("/api/habits/", data, format="json")
    assert response.status_code == 201
    assert response.data["name"] == "New Habit"
    assert response.data["is_active"] is True

# Удаление привычки
@pytest.mark.django_db
def test_delete_habit():
    user = User.objects.create_user(username="testuser", password="pass")
    habit = Habit.objects.create(name="Habit to delete", user=user)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.delete(f"/api/habits/{habit.id}/")
    assert response.status_code == 204
    assert not Habit.objects.filter(id=habit.id).exists()

# Получение списка целей и создание цели
@pytest.mark.django_db
def test_goal_list_and_create():
    user = User.objects.create_user(username="testuser", password="pass")
    client = APIClient()
    client.force_authenticate(user=user)

    # Создаем цель
    data = {
        "title": "Read Books",
        "description": "Read 12 books this year",
        "start_date": str(date.today()),
        "end_date": str(date.today() + timedelta(days=365)),
        "target_value": 12,
        "current_value": 0,
        "user": user.id
    }
    response = client.post("/api/goals/", data, format="json")
    assert response.status_code == 201
    assert response.data["title"] == "Read Books"

    # Получаем список целей
    response = client.get("/api/goals/")
    assert response.status_code == 200
    assert len(response.data) >= 1
