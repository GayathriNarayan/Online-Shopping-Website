from django.contrib import admin
from onlineapp.models import CustomerInfo
from onlineapp.models import ProductClassification,Product,Size,ProductSize
from onlineapp.models import Order,OrderDetail

#Customer details
admin.site.register(CustomerInfo)

#Category and product
admin.site.register(ProductClassification)
admin.site.register(Product)
admin.site.register(Size)
admin.site.register(ProductSize)

#Order and Order details
admin.site.register(Order)
admin.site.register(OrderDetail)
