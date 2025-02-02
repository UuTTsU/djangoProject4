from django.urls import path
from .views import (
    WorkoutPlanListCreateView,
    WorkoutPlanDetailView,
    WorkoutSessionListCreateView,
    WorkoutSessionDetailView
)

urlpatterns = [
    path('workout-plans/', WorkoutPlanListCreateView.as_view(), name='workout_plan_list_create'),
    path('workout-plans/<int:pk>/', WorkoutPlanDetailView.as_view(), name='workout_plan_detail'),
    path('workout-plans/<int:pk>/sessions/', WorkoutSessionListCreateView.as_view(), name='workout_session_list_create'),
    path('workout-sessions/<int:pk>/', WorkoutSessionDetailView.as_view(), name='workout_session_detail')
]
