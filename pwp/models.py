from django.contrib.auth import get_user_model
from django.db import models
from database.models import Goals, Exercise

class WorkoutPlan(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    frequency = models.IntegerField()
    goal = models.ForeignKey(Goals, on_delete=models.SET_NULL, null=True)
    exercises = models.ManyToManyField(Exercise)


class WorkoutSession(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name="sessions")
    date = models.DateField()  # Stores the session date
    session_duration = models.IntegerField()  # Duration in minutes

    def __str__(self):
        return f"Session for {self.workout_plan.user} on {self.date} ({self.session_duration} min)"