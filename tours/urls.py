from django.urls import path
from . import views

app_name = 'tours'

urlpatterns = [
    path('categories/',views.CategoryListCreatedView.as_view(), name='category-list'),
    path('categories/<slug:category_slug>/product',views.product_by_category, name='product-by-category'),
    path('categories/<slug:slug>',views.CategoryDatailView.as_view(), name='category-datail'),

    path('',views.ProductListCreateView.as_view(),name='product-list'),
    path('my-product/',views.MyProductView.as_view(),name='my-product'),
    path('recent/',views.recent_product,name='recent-product'),
    path('<slug:slug>/',views.ProductDatailView.as_view(),name='product-datail')
]   
