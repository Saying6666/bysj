from django.urls import path
from .views import *

urlpatterns = [
    path('', index_view, name='index'),
    
    path('chat_with_baidu_unit/',chat_with_baidu_unit, name='chat_with_baidu_unit'),
]