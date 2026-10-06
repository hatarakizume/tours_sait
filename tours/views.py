from rest_framework import generics,permissions,status,filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import get_object_or_404
from .models import Category, Product

from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CategorySerializer,
    ProductCreateUpdateSerializer,
    ProductListSerializer,
    ProductDatailSerializer
)
from django.db.models import Q
# Create your views here.

class CategoryListCreatedView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

class CategoryDatailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.odjects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author', 'status']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Product.objects.select_related('author','category')

        if not self.request.user.is_authenticated:
            queryset = Product.object.filter(status='punlished')    
        else:
            queryset = queryset.filter(
                Q(status='published') | Q(author=self.request.user)
            )
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'Post':
            return ProductCreateUpdateSerializer
        return ProductListSerializer

class ProductDatailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('author','category')
    serializer_class = ProductDatailSerializer
    permission_classes = IsAuthorOrReadOnly
    lookup_field = 'slug'

    def get_serializer_class(self):
            if self.request.method in ['PUT','PUTCH']:
                return ProductCreateUpdateSerializer
            return ProductDatailSerializer

class MyProductView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = ['category','status']
    search_fields = ['title','content']
    ordering_foelds = ['created_at','updated_at']
    ordering = ['-creaetd_at']

    def get_queryset(self):
        return Product.objects.filter(
            author = self.request.user
        ).select_related('author', 'category')

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def product_by_category(request,category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = Product.objects.filter(
        category=category,
        status='published',
    ).select_related('author', 'category').order_by('-created_at')
    serializer = ProductListSerializer(product,many=True,context={'request': request})
    return Response({
        'category': CategorySerializer(category).data,
        'product': serializer.data
    })

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def recent_product(request):
    product = Product.objects.filter(
        status='published',
    ).select_related('author', 'category').order_by('-created_at')[:10]
    serializer = ProductListSerializer(product,many=True,context={'request': request})
    return Response(serializer.data)