from django.urls import path
from .views import prediction_view

app_name = 'prediction'

urlpatterns = [
    path('hands-unmuted/', prediction_view, name='hands_unmuted'),
]