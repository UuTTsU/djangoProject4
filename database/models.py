from django.db import models

class Exercise(models.Model):
    exercise_id = models.AutoField(primary_key=True)  # Explicit primary key
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructions = models.TextField()
    target_muscles = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Goals(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return  self.name