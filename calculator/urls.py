from django.urls import path
from .views import CalculateBMIView, RecommendationsView, ProgressListCreateView, RegisterView, AdminUserReportListView,AdminUserReportDetailView, ProfileView

urlpatterns = [
    path('calculate_bmi/', CalculateBMIView.as_view(), name='calculate-bmi'),
    path('recommendations/<str:category>/', RecommendationsView.as_view(), name='recommendations'),
    path('progress/', ProgressListCreateView.as_view(), name='progress'),
    path('register/', RegisterView.as_view(), name='register'),

    path('admin/users/',      AdminUserReportListView.as_view(),   name='admin-users-list'),
    path('admin/users/<int:pk>/', AdminUserReportDetailView.as_view(), name='admin-user-detail'),

    path('profile/', ProfileView.as_view(), name='profile'),
]