from django.urls import path
from . import views

urlpatterns = [
    path('', views.quote_of_the_day, name='quote_of_the_day'),
    path('quote/', views.quote_of_the_day, name='quote'),
    path('show_all/', views.show_all, name='show_all'),
    path('about/', views.about, name='about'),
]