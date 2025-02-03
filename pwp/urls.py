from django.urls import path
from .views import (
    WorkoutPlanListCreateView,
    WorkoutPlanDetailView,
    WorkoutSessionListCreateView,
    WorkoutSessionDetailView,
    WeightTrackingListCreateView,
    WeightTrackingDetailView,
    FitnessGoalListCreateView,
    FitnessGoalDetailView,
    StartWorkoutView,
    NextExerciseView,
    CompleteExerciseView,
    AdjustExerciseView
)

urlpatterns = [
    path('workout-plans/', WorkoutPlanListCreateView.as_view(), name='workout_plan_list_create'),
    path('workout-plans/<int:pk>/', WorkoutPlanDetailView.as_view(), name='workout_plan_detail'),
    path('workout-plans/<int:pk>/sessions/', WorkoutSessionListCreateView.as_view(), name='workout_session_list_create'),
    path('workout-sessions/<int:pk>/', WorkoutSessionDetailView.as_view(), name='workout_session_detail'),
    path('weight-tracking/', WeightTrackingListCreateView.as_view(), name = 'weight_tracking_list_create'),
    path('weight-tracking/<int:pk>/', WeightTrackingDetailView.as_view(), name='weight_tracking_detail'),
    path('fitness-goal/', FitnessGoalListCreateView.as_view(), name='fitness_goal_list_create'),
    path('fitness-goal/<int:pk>/', FitnessGoalDetailView.as_view(), name='fitness_goal_detail'),
    path('workout-mode/start/<int:session_id>/', StartWorkoutView.as_view(), name='start_workout'),
    path('workout-mode/next-exercise/<int:session_id>/', NextExerciseView.as_view(), name='next_exercise'),
    path('workout-mode/complete-exercise/<int:progress_id>/', CompleteExerciseView.as_view(), name='complete_exercise'),
    path('workout-mode/adjust-exercise/<int:progress_id>/', AdjustExerciseView.as_view(), name='adjust_exercise'),
]




