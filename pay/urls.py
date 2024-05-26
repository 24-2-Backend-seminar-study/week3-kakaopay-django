from django.urls import path
from .views import PayReadyView, PayApproveView


app_name = "pay"
urlpatterns = [
    # CBV url path
    path("ready/", PayReadyView.as_view()),
    path("approve/", PayApproveView.as_view()),
]