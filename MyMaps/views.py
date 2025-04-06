from django.shortcuts import render
from django.http import HttpResponse
from MyMaps.models import LandParcel, LeaseAgreement, LeasePayment
# Create your views here.

def index(request):
    my_dict = {'insert_map': "This is the map placeholder"}
    return render(request, 'MyMaps/index.html', context=my_dict)
    
def home(request):
    return HttpResponse("This shoudde be HTML content for the home page") 

def land_parcel_list(request):
    return HttpResponse("This is the list of all available Land Parcels")

def help (request):
    return render(request, 'MyMaps/help.html')
