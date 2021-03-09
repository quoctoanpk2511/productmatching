from django.urls import path, re_path
from . import views
from .views import (
    ProductsView
)

urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    path('products', ProductsView.as_view(), name='products'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]