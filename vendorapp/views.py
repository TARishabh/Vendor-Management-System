from rest_framework import generics
from .models import Vendor,PurchaseOrder
from .serializers import VendorPostSerializer,VendorRetrieveSerializer,PurchaseOrderCreateUpdateSerializer,PurchaseOrderDetailSerializer,PurchaseOrderUpdateSerializer
from .models import Vendor, HistoricalPerformance
from .serializers import HistoricalPerformanceSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import VendorPerformanceSerializer
from rest_framework import status
from django.utils import timezone



class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    def get_serializer_class(self):
        """
        Selects the appropriate serializer based on the request method.
        """
        if self.request.method == 'POST':
            return VendorPostSerializer
        return VendorRetrieveSerializer

class VendorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    def get_serializer_class(self):
        """
        Selects the appropriate serializer based on the request method.
        """
        if self.request.method in ['PUT', 'PATCH']:
            return VendorPostSerializer
        return VendorRetrieveSerializer
    
class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    def get_serializer_class(self):
        """
        Selects the appropriate serializer based on the request method.
        """
        if self.request.method == 'POST':
            return PurchaseOrderCreateUpdateSerializer
        return PurchaseOrderDetailSerializer

class PurchaseOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    def get_serializer_class(self):
        """
        Selects the appropriate serializer based on the request method.
        """
        if self.request.method in ['PUT', 'PATCH']:
            return PurchaseOrderUpdateSerializer
        return PurchaseOrderDetailSerializer
    
# class VendorPerformanceView(generics.RetrieveAPIView):
#     queryset = Vendor.objects.all()
#     serializer_class = HistoricalPerformanceSerializer

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         historical_performance = HistoricalPerformance.objects.filter(vendor=instance)
#         serializer = self.get_serializer(historical_performance, many=True)
#         return Response(serializer.data)

class VendorPerformanceAPIView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            serializer = VendorPerformanceSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class AcknowledgePurchaseOrderAPIView(APIView):
    def post(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()
            # Trigger recalculation of average_response_time
            # Your logic to recalculate average_response_time here
            return Response(status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)