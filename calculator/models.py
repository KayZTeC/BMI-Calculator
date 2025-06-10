from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height_cm = models.FloatField()
    weight_kg = models.FloatField()
    fitness_goal = models.CharField(max_length=100)

class BMIRecord(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bmi_records'      # ← add this
    )
    date = models.DateTimeField(auto_now_add=True)
    height_cm = models.FloatField()
    weight_kg = models.FloatField()
    bmi = models.FloatField()

class FitnessRecommendation(models.Model):
    category = models.CharField(max_length=50)
    recommendation_text = models.TextField()

    def __str__(self):
        return f"{self.category}: {self.recommendation_text[:30]}..."
    
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Progress(models.Model):
    user = models.ForeignKey(
        User,
        related_name='progress_entries',
        on_delete=models.CASCADE
    )
    bmi = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.bmi} at {self.timestamp:%Y-%m-%d %H:%M}"
