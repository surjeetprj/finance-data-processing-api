from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FinancialRecordViewSet, DashboardSummaryView

router = DefaultRouter()
router.register(r'records', FinancialRecordViewSet, basename='financial-record')

urlpatterns = [
    # custom Dashboard endpoint
    path('dashboard/summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),

    # Generated router URLs
    path('', include(router.urls)),
]

