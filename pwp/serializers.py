from rest_framework import serializers
from .models import WorkoutPlan, WorkoutSession, WeightTracking, FitnessGoal, WorkoutProgress
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

class WeightTrackingSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeightTracking
        fields = ['id', 'user', 'weight', 'date']
        read_only_fields = ['id', 'user', 'date']

    def create(self, validated_data):

        user = self.context['request'].user
        weight_entry = WeightTracking.objects.create(user=user, **validated_data)


        fitness_goals = FitnessGoal.objects.filter(user=user, goal_type__name__in=["Weight Loss", "Muscle Gain"],
                                                   is_completed=False)
        for goal in fitness_goals:
            if goal.goal_type.name == "Weight Loss":
                goal.progress = max(0, user.weighttracking_set.order_by('-date').first().weight - goal.target_value)
            elif goal.goal_type.name == "Muscle Gain":
                goal.progress = max(0, goal.target_value - user.weighttracking_set.order_by('-date').first().weight)

            if goal.progress >= abs(goal.target_value - user.weighttracking_set.earliest('date').weight):
                goal.is_completed = True

            goal.save()

        return weight_entry


class FitnessGoalSerializer(serializers.ModelSerializer):


    goal_type = serializers.CharField(source="goal_type.name", read_only=True)

    class Meta:
        model = FitnessGoal
        fields = ['id', 'user', 'goal_type', 'target_value', 'progress', 'is_completed', 'created_at']
        read_only_fields = ['id', 'user', 'progress', 'is_completed', 'created_at']

    def create(self, validated_data):

        user = self.context['request'].user
        return FitnessGoal.objects.create(user=user, **validated_data)



class WorkoutProgressSerializer(serializers.ModelSerializer):


    exercise_name = serializers.CharField(source="exercise.name", read_only=True)  # Show exercise name instead of ID
    start_time = serializers.DateTimeField(read_only=True)  # Auto-set start time
    end_time = serializers.DateTimeField(required=False, allow_null=True)  # User can update end time

    class Meta:
        model = WorkoutProgress
        fields = [
            "id", "workout_session", "exercise", "exercise_name",
            "planned_sets", "planned_reps", "actual_sets", "actual_reps",
            "start_time", "end_time", "is_completed", "notes"
        ]
        read_only_fields = ["planned_sets", "planned_reps", "start_time"]

    def create(self, validated_data):

        exercise = validated_data["exercise"]
        validated_data["planned_sets"] = exercise.default_sets
        validated_data["planned_reps"] = exercise.default_reps
        return super().create(validated_data)