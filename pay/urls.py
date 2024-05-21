from django.urls import path
from .views import PayReadyView


app_name = "account"
urlpatterns = [
    # CBV url path
    path("payready/", PayReadyView.as_view()),
]