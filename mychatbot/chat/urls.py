from django.urls import path
from .views import chat_view, index_view

urlpatterns = [
    path('', index_view, name='index'),
    path('chat/', chat_view, name='chat_view'),
]