from django.contrib import admin
from .models import (
    Product,
    Vendor,
)

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'vendor_id', 'cluster_label', 'cluster_id', 'new_cluster')

admin.site.register(Vendor)
