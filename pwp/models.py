from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

from database.models import Goals, Exercise
from user.models import CustomUser

class WorkoutPlan(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    frequency = models.IntegerField()
    goal = models.ForeignKey(Goals, on_delete=models.SET_NULL, null=True)
    exercises = models.ManyToManyField(Exercise)


class WorkoutSession(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name="sessions")
    date = models.DateField()
    session_duration = models.IntegerField()

    def __str__(self):
        return f"Session for {self.workout_plan.user} on {self.date} ({self.session_duration} min)"



class WeightTracking(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    weight = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.email} - {self.weight}kg on {self.date}"

class FitnessGoal(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    goal_type = models.ForeignKey(Goals, on_delete=models.CASCADE)
    target_value = models.FloatField()
    progress = models.FloatField(default=0.0)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.email} - {self.goal_type.name} ({self.progress}/{self.target_value})"

class WorkoutProgress(models.Model):
    workout_session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name="progress")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    planned_sets = models.IntegerField(default=3)
    planned_reps = models.IntegerField(default=10)
    actual_sets = models.IntegerField(null=True, blank=True)
    actual_reps = models.IntegerField(null=True, blank=True)
    start_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.planned_sets = self.exercise.default_sets
            self.planned_reps = self.exercise.default_reps
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.workout_session.user} - {self.exercise.name} ({'Completed' if self.is_completed else 'In Progress'})"
