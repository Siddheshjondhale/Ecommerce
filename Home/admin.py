from django.contrib import admin

from Home.views import Qrdetails
from .models import Mens,order,detailsqr,Review
# Register your models here
admin.site.register(Mens)
admin.site.register(order)
admin.site.register(detailsqr)

admin.site.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id','user','mensProduct','rate','created_at']
    readonly_fields = ['created_at']