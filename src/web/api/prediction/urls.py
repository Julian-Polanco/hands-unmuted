from django.urls import path

app_name = 'prediction'


urlpatterns = [
    path('hands-unmuted/',  name='hands_unmuted'),
]