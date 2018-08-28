from django.contrib import admin
from app import models
admin.site.register(models.User)
# admin.site.register(News)
admin.site.register(models.Goods)
admin.site.register(models.Order)
admin.site.register(models.Shoppingcar)

# Register your models here.
