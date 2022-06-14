from django.contrib import admin
from onlineapp.models import CustomerInfo
from onlineapp.models import ProductClassification,Product,Size,ProductSize
from onlineapp.models import Order,OrderDetail
from onlineapp.models import Product_Review

#Customer details
admin.site.register(CustomerInfo)

#Category ,Review and Product
admin.site.register(ProductClassification)
admin.site.register(Product)
admin.site.register(Size)
admin.site.register(ProductSize)
admin.site.register(Product_Review)

#Order and Order details
admin.site.register(Order)
admin.site.register(OrderDetail)
