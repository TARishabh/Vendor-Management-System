from rest_framework import serializers
from vendorapp.models import Vendor,PurchaseOrder,HistoricalPerformance
import uuid
import re
from django.utils import timezone
from datetime import timedelta


class VendorPostSerializer(serializers.ModelSerializer):
    """
    Serializer for Vendor model
    """
    class Meta(object):
        model = Vendor
        fields = ['id','name','contact_details','address',]
        read_only_fields = ['id','on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate']


    def validate_contact_details(self, value):
        if value:
            pattern = re.compile("^[6-9]\d{9}$")
            if not pattern.match(value):
                raise serializers.ValidationError("Phone Number Not accepted")
        return value

    def create(self, validated_data):
        # Generate a unique vendor code
        validated_data['vendor_code'] = str(uuid.uuid4())
        return super().create(validated_data)
    
class VendorRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer for Vendor model
    """
    class Meta(object):
        model = Vendor
        fields = ['id','name','contact_details','address','on_time_delivery_rate','quality_rating_avg','average_response_time','fulfillment_rate',]


class PurchaseOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating']
        # read_only_fields = ['id', 'po_number', 'order_date', 'issue_date', 'delivery_date']  # Ensure delivery_date is read-only

class PurchaseOrderCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['id','items', 'quantity',]
        read_only_fields = ['id', 'order_date', 'issue_date', 'acknowledgment_date']

    def create(self, validated_data):
        # Generate po_number using UUID
        validated_data['po_number'] = str(uuid.uuid4())
        # Set order_date to current time
        validated_data['order_date'] = timezone.now()
        validated_data['issue_date'] = timezone.now()
        # Set delivery_date to 7 days after order_date
        validated_data['delivery_date'] = validated_data['order_date'] + timedelta(days=7)
        return super().create(validated_data)
    
class PurchaseOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'vendor', 'delivery_date', 'status', 'quality_rating']
        read_only_fields = ['id', 'order_date', 'issue_date', 'acknowledgment_date']

    def update(self, instance, validated_data):
        # Update acknowledgment_date if status changes from 'NA' to 'Cancel' or 'Pending'
        # if instance.status == 'NA' and validated_data.get('status') in ['canceled', 'pending']:
        #     instance.acknowledgment_date = timezone.now()

        # Updating other fields
        instance.vendor = validated_data.get('vendor', instance.vendor)
        instance.delivery_date = validated_data.get('delivery_date', instance.delivery_date)
        instance.status = validated_data.get('status', instance.status)
        instance.quality_rating = validated_data.get('quality_rating', instance.quality_rating)
        instance.save()
        return instance
    
class PurchaseOrderAcknowledgeSerializer(serializers.ModelSerializer):
    def validate_acknowledgment_date(self, value):
        """
        Check if acknowledgment_date is not less than today's date.
        """
        if value.date() < timezone.now().date():
            raise serializers.ValidationError("Acknowledgment date cannot be in the past.")
        return value
    
    class Meta:
        model = PurchaseOrder
        fields = ['acknowledgment_date']

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = ['date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']

class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
