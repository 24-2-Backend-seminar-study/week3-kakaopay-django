from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Pay(models.Model):
  tid = models.CharField(max_length=100)
  partner_order_id = models.CharField(max_length=100, default='')
  partner_user_id = models.CharField(max_length=100, default='')
  created_at = models.DateTimeField(default=timezone.now)
  buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pay_buyer', null=True)