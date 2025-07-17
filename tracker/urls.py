from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, GoalViewSet, HabitActionViewSet, GoalProgressViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'habits', HabitViewSet)
router.register(r'goals', GoalViewSet)
router.register(r'habit-actions', HabitActionViewSet)
router.register(r'goal-progress', GoalProgressViewSet)

urlpatterns = [
    path('', include(router.urls)),
]