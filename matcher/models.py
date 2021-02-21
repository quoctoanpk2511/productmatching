from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255)
    vendor_id = models.IntegerField()
    cluster_id = models.IntegerField()
    cluster_label = models.CharField(max_length=255)
    category_id = models.IntegerField()
    category_label = models.CharField(max_length=255)
    new_cluster = models.IntegerField(null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('product-detail', args=[str(self.id)])

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    home_page = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('vendor-detail', args=[str(self.id)])
