from django.urls import path
from . import views

app_name = 'prediction'

urlpatterns = [
    path('', views.prediction_view, name='hands_unmuted'),
    path('single/', views.single_prediction_view, name='single_prediction'),
    path('text-to-signs/', views.text_to_signs_view, name='text_to_signs'),

]