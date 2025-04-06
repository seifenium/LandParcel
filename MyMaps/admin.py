from django.contrib import admin
from MyMaps.models import LandParcel, LeaseAgreement, LeasePayment

# Register your models here.
admin.site.register(LandParcel)
admin.site.register(LeaseAgreement)
admin.site.register(LeasePayment)