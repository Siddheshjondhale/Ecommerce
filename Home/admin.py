from django.contrib import admin

from Home.views import Qrdetails
from .models import Mens,order,detailsqr
# Register your models here
admin.site.register(Mens)
admin.site.register(order)
admin.site.register(detailsqr)