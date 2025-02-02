from rest_framework import serializers
from .models import WorkoutPlan, WorkoutSession
from database.models import Exercise, Goals

class WorkoutPlanSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    goal = serializers.PrimaryKeyRelatedField(queryset=Goals.objects.all())
    exercises = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all(), many=True)

    class Meta:
        model = WorkoutPlan
        fields = ['id', 'user', 'frequency', 'goal', 'exercises']

class WorkoutSessionSerializer(serializers.ModelSerializer):
    workout_plan = serializers.PrimaryKeyRelatedField(queryset=WorkoutPlan.objects.all())

    class Meta:
        model = WorkoutSession
        fields = ['id', 'workout_plan', 'date', 'session_duration']
