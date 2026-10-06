from django.db import models
from django.utils.text import slugify
from django.conf import settings
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_teble = 'categories'
        verbose_name = 'Category'
        verbose_name_polural = 'Categories'
        ordering = ['name']

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):

    STATUS_CHOICES = [
        ('draft','Draft'),
        ('published','Published')
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,blank=True, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='posts')
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='published')
    content = models.TextField(blank=True)
    main_image = models.ImageField(upload_to='products/tours/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    total_places = models.PositiveIntegerField(default=0)
    available_places = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'posts'
        verbose_name = 'Post'
        verbose_name_polural = 'Posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status','-created_at']),
            models.Index(fields=['category','-created_at']),
            models.Index(fields=['author','-created_at']),
        ]

    def save(self,*args,**kwargs):
            if not self.slug:
                self.slug = slugify(self.title)
            super().save(*args,**kwargs)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
         return reversed('-post-datail',kwargs={'slug':self.slug})

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images')
    image = models.ImageField(upload_to='products/extra/')