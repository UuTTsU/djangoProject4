from django.db import models

class Exercise(models.Model):
    exercise_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructions = models.TextField()
    target_muscles = models.CharField(max_length=200)
    default_sets = models.IntegerField(default=3)
    default_reps = models.IntegerField(default=10)
    default_rest = models.IntegerField(default=60)

    def __str__(self):
        return f'{self.name} - {self.default_sets} x {self.default_reps} times'

class Goals(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return  self.name