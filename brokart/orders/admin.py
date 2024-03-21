from django.contrib import admin
from .models import Order,Ordered_item

# Register your models here.
admin.site.register(Order)
admin.site.register(Ordered_item)
