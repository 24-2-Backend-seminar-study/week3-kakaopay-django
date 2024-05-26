from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json

from .models import Pay
from .serializers import PaySerializer

from django.conf import settings

pay_key = settings.KAKAO_PAY_KEY
cid = settings.CID
payready_url = 'https://open-api.kakaopay.com/online/v1/payment/ready'
payapprove_url = 'https://open-api.kakaopay.com/online/v1/payment/approve'

class PayReadyView(APIView):
  def post(self, request):
    pay_data = request.data
    buyer = request.user
    if not buyer.is_authenticated:
      return Response({"detail": "please signin."}, status=status.HTTP_401_UNAUTHORIZED)
    pay_data['cid'] = cid
    pay_header = {
      'Content-Type': 'application/json',
      'Authorization': f'SECRET_KEY {pay_key}'
    }
    pay_data = json.dumps(pay_data)
    response = requests.post(payready_url, headers=pay_header, data=pay_data)
    response_data = response.json()
    if response.status_code == 200:
      # tid, partner_user_id, partner_order_id DB에 저장
      Pay.objects.create(
        tid=response_data['tid'],
        partner_order_id=request.data['partner_order_id'],
        partner_user_id=request.data['partner_user_id'],
        buyer=buyer,
        item_name=request.data['item_name'],
        total_amount=request.data['total_amount'],
        item_amount=request.data['quantity'],
      )
    return Response(response.json(), status=response.status_code)
  
class PayApproveView(APIView):
  def post(self, request):
    pg_token = request.data['pg_token']
    tid = request.data['tid']
    pay_hist = Pay.objects.get(tid=tid)
    print(pg_token, tid)
    pay_header = {
      'Content-Type': 'application/json',
      'Authorization': f'SECRET_KEY {pay_key}'
    }
    pay_data = {
      'cid': cid,
      'tid': tid,
      'partner_order_id': pay_hist.partner_order_id,
      'partner_user_id': pay_hist.partner_user_id,
      'pg_token': pg_token
    }
    pay_data = json.dumps(pay_data)
    response = requests.post(payapprove_url, headers=pay_header, data=pay_data)
    print("response", response.json())
    return Response(response.json(), status=response.status_code)
  
class PayHistoryView(APIView):
  def get(self, request):
    buyer = request.user
    if not buyer.is_authenticated:
      return Response({"detail": "please signin."}, status=status.HTTP_401_UNAUTHORIZED)
    pay_hist = Pay.objects.filter(buyer=buyer)
    serializer = PaySerializer(pay_hist, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)