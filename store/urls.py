from django.urls import path
from .views import ProductListView, ProductDetailView, AboutView, buy_items
from . import views

urlpatterns = [
    path('', ProductListView.as_view(), name='base'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('about/', AboutView.as_view(), name='about'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('buy_items/', buy_items, name='buy_items'),
]
