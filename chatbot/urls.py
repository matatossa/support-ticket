from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chatbot_html_view, name='chatbot'),  
      path('redirect/', views.redirect_to_dashboard, name='redirect_to_dashboard'),
]