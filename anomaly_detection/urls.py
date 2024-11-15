from django.urls import path,include
#from .views import anomaly_view
from . import views

urlpatterns = [
    path('dashboard/', views.anomaly_view, name='anomaly_view'),  # Keep only one definition
]
