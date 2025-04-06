#This is the My Maps App URL Configuration
from . import views
from django.urls import path

# Define namespace for the app
app_name = 'MyMaps'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('land_parcel_list/', views.land_parcel_list, name='land_parcel_list'),
    path('help/', views.help, name='help'),
    path('', views.index, name='index'),
]