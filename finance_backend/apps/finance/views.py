from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsAnalyst, IsEditor
from .models import FinancialRecord
from .serializers import FinancialRecordSerializer # pyright: ignore[reportMissingImports]
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes



class FinancialRecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Financial Records with Filtering, Searching, and Sorting.
    
    Access is strictly controlled by custom RBAC permissions.
    """
    queryset = FinancialRecord.objects.all()
    serializer_class = FinancialRecordSerializer
    
    # User must be logged in, AND must match one of our three roles
    permission_classes = [IsAuthenticated, (IsAdmin | IsAnalyst | IsEditor)]

    # Enable the filter backends
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    
    # Exact match filtering (e.g., ?transaction_type=INCOME)
    filterset_fields = ['transaction_type', 'category']
    
    # Sorting (e.g., ?ordering=-amount or ?ordering=date)
    ordering_fields = ['date', 'amount']
    
    # Text searching (e.g., ?search=electricity)
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        """
        When a user sends a POST request, automatically attach 
        their user account to the new financial record.
        """
        serializer.save(user=self.request.user)
    
    # Explicitly documenting the GET (list) method
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='ordering',
                description='Which field to use when ordering the results. \n\n**Allowed values:** \n* `date` (Ascending) \n* `-date` (Descending) \n* `amount` (Ascending) \n* `-amount` (Descending)',
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name='transaction_type',
                description='Filter records by the exact type of transaction.',
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                enum=['INCOME', 'EXPENSE']
            ),
            OpenApiParameter(
                name='category',
                description='Filter records by exact category name (e.g., `Utilities`, `Salary`, `Housing`). Note: This is case-sensitive.',
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        # We don't change any logic, we just pass it to the default DRF behavior
        return super().list(request, *args, **kwargs)
        
        
class DashboardSummaryView(APIView):
    """
    API endpoint that returns aggregated dashboard data:
    Total Income, Total Expenses, Net Balance, and Categorized Expenses.
    Supports date range filtering (?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD).
    """
    permission_classes = [IsAuthenticated, (IsAdmin | IsAnalyst | IsEditor)]

    def get(self, request):
        # start with all records
        queryset = FinancialRecord.objects.all()
        
        # Apply Data Filtering (if the user provided in the URL)
        start_date =request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
            
        # Calculate Totals
        total_income = queryset.filter(transaction_type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = queryset.filter(transaction_type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
    
        net_balance = total_income - total_expenses
        
        # Categorized Expenses
        # This groups the expenses by ctegory and sums them up
        categorized_expenses = queryset.filter(transaction_type='EXPENSE') \
            .values('category') \
            .annotate(total=Sum('amount')) \
            .order_by('-total')
        
        # Recent Activities (Last 5 Transections)
        recent_activity = queryset.order_by('-created_at') \
            .values('title', 'amount', 'transaction_type', 'date')[:5]
        
        # Monthly Trends    
        monthly_trends = queryset.annotate(month=TruncMonth('date')) \
            .values('month') \
            .annotate(
                income = Sum('amount', filter=Q(transaction_type='INCOME')),
                expense = Sum('amount', filter=Q(transaction_type='EXPENSE'))
                ) \
            .order_by('month')
        
        # Clean up the None values in trends (if a month had no income/expense)
        cleaned_trends = [
            {
                "month" : trend['month'].strftime('%y-%m') if trend ['month'] else None,
                "income": trend['income'] or 0,
                "expense": trend['expense'] or 0
            } 
            for trend in monthly_trends
        ]
        
        
        # Return the perfecty formatted JSON
        return Response({
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': net_balance,
            'categorized_expenses': list(categorized_expenses),
            "recent_activity": list(recent_activity),
            "monthly_trends": cleaned_trends
        })
        
        

    