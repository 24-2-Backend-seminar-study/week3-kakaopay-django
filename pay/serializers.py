from rest_framework.serializers import ModelSerializer
from .models import Pay

class PaySerializer(ModelSerializer):
    class Meta:
        model = Pay
        fields = ['buyer', 'item_name', 'total_amount', 'item_amount']