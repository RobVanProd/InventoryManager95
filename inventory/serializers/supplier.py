from rest_framework import serializers
from ..models.supplier import Supplier, SupplierContact


class SupplierContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierContact
        fields = [
            'id', 'name', 'role', 'email', 'phone',
            'is_primary', 'supplier'
        ]
        read_only_fields = ['id']


class SupplierSerializer(serializers.ModelSerializer):
    additional_contacts = SupplierContactSerializer(many=True, read_only=True)
    
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'code', 'contact_name', 'email',
            'phone', 'address', 'website', 'tax_id',
            'reliability_rating', 'average_lead_time',
            'on_time_delivery_rate', 'is_active',
            'created_at', 'updated_at', 'notes',
            'additional_contacts'
        ]
        read_only_fields = [
            'id', 'reliability_rating', 'average_lead_time',
            'on_time_delivery_rate', 'created_at', 'updated_at'
        ]

    def validate_code(self, value):
        """Ensure supplier code is unique and properly formatted"""
        if not value.isalnum():
            raise serializers.ValidationError(
                "Supplier code must contain only letters and numbers"
            )
        return value.upper()
