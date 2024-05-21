from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json

from django.conf import settings

pay_key = settings.KAKAO_PAY_KEY
cid = settings.CID
payready_url = 'https://open-api.kakaopay.com/online/v1/payment/ready'

class PayReadyView(APIView):
  def post(self, request):
    pay_data = request.data
    pay_data['cid'] = cid
    print("pay_data: ", pay_data)
    headers = {
      'Content-type': 'application/json',
      'Authorization': f'SECRET_KEY {pay_key}'
    }
    response = requests.post(payready_url, headers=headers, data=json.dumps(pay_data))
    print("response: ", response.json())
    return Response(response.json(), status=response.status_code)