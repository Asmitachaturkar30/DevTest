from django.urls import path
from .views import * 

urlpatterns = [
    path('', upload_file, name='upload_file'),
]