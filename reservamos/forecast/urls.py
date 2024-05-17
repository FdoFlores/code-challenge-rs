from django.urls import path
from .views import ForecastView

urlpatterns = [
    path('<str:city>', ForecastView.as_view(), name='test'),
]