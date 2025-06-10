from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import BMIRecord, FitnessRecommendation
from .serializers import BMICalculateSerializer, BMIRecordSerializer, FitnessRecommendationSerializer

# 2.1 Calculate BMI & Save Record
def get_bmi_category(bmi):
    if bmi < 18.5:
        return 'Underweight'
    if bmi < 25:
        return 'Normal'
    if bmi < 30:
        return 'Overweight'
    return 'Obese'

class CalculateBMIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = BMICalculateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        h = serializer.validated_data['height_cm']
        w = serializer.validated_data['weight_kg']
        bmi = w / ((h / 100) ** 2)
        category = get_bmi_category(bmi)
        # Save record
        BMIRecord.objects.create(
            user=request.user,
            height_cm=h,
            weight_kg=w,
            bmi=round(bmi, 2)
        )
        return Response({'bmi': round(bmi, 2), 'category': category}, status=status.HTTP_200_OK)

# 2.2 List Recommendations by Category
class RecommendationsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FitnessRecommendationSerializer
    lookup_field = 'category'

    def get_queryset(self):
        return FitnessRecommendation.objects.filter(category__iexact=self.kwargs['category'])

# 2.3 Progress Tracking: list & create
class ProgressListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BMIRecordSerializer

    def get_queryset(self):
        return BMIRecord.objects.filter(user=self.request.user).order_by('date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework import generics, permissions
from .serializers import UserRegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = UserRegisterSerializer.Meta.model.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]    # ← let anyone hit this endpoint

# calculator/views.py
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import AdminUserReportSerializer

User = get_user_model()

class AdminUserReportListView(generics.ListAPIView):
    queryset          = User.objects.all()
    serializer_class  = AdminUserReportSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminUserReportDetailView(generics.RetrieveAPIView):
    queryset          = User.objects.all()
    serializer_class  = AdminUserReportSerializer
    permission_classes = [permissions.IsAdminUser]

from rest_framework import generics, permissions
from .serializers import ProfileSerializer

class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
