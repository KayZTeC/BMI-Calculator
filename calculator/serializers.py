from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, BMIRecord, FitnessRecommendation

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['height_cm', 'weight_kg', 'fitness_goal']

class BMICalculateSerializer(serializers.Serializer):
    height_cm = serializers.FloatField()
    weight_kg = serializers.FloatField()

class BMIRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BMIRecord
        fields = ['id', 'date', 'height_cm', 'weight_kg', 'bmi']
        read_only_fields = ['id', 'date', 'bmi']

class FitnessRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessRecommendation
        fields = ['category', 'recommendation_text']


from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="This email is already taken.")]
    )
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )


# calculator/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Progress  # your model tracking user BMI over time

User = get_user_model()

class ProgressSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(source='timestamp', format='%Y-%m-%d')

    class Meta:
        model = Progress
        fields = ['id', 'bmi', 'date']


# calculator/serializers.py
from .models import BMIRecord
from .serializers import BMIRecordSerializer   # adjust your imports

class AdminUserReportSerializer(serializers.ModelSerializer):
    latest_bmi       = serializers.SerializerMethodField()
    progress_history = BMIRecordSerializer(
                          many=True,
                          source='bmi_records',    # ← point here
                          read_only=True
                       )

    class Meta:
        model  = User
        fields = [
          'id','username','email','date_joined','last_login',
          'latest_bmi','progress_history'
        ]

    def get_latest_bmi(self, user):
        last = user.bmi_records.order_by('-date').first()
        return last.bmi if last else None
