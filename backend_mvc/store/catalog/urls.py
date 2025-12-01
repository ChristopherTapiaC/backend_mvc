from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Productos
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # Clientes
    path('clients/', views.client_list, name='client_list'),
    path('clients/create/', views.client_create, name='client_create'),
    path('clients/<int:pk>/edit/', views.client_edit, name='client_edit'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),

    # Ventas (flujo nuevo con carrito)
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/<int:pk>/delete/', views.sale_delete, name='sale_delete'),
    path('sales/new/', views.sale_start, name='sale_start'),
    path('sales/cart/', views.sale_cart, name='sale_cart'),
    path('sales/cart/remove/<int:index>/', views.sale_item_remove, name='sale_item_remove'),
    path('sales/confirm/', views.sale_confirm, name='sale_confirm'),
    path('sales/cancel/', views.sale_cancel, name='sale_cancel'),

    # Edición de ventas ya confirmadas
    path('sales/<int:sale_id>/edit/', views.sale_edit, name='sale_edit'),
    path('sales/<int:sale_id>/detail/<int:detail_id>/delete/', views.sale_detail_delete, name='sale_detail_delete'),

]
