from rest_framework import serializers
from django.utils import timezone
from .models import FinancialRecord

class FinancialRecordSerializer(serializers.ModelSerializer):
    # Display the username instead of just the ID, and make it read-only
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = FinancialRecord
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    # Custom Validation
    # Amount must be greater than zero
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("The transaction amount must be strictly greater than zero.")
        return value

    # Date cannot be in the future
    def validate_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("The transaction date cannot be in the future.")
        return value