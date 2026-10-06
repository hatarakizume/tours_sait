# from django.db import models
# from django.conf import settings
# from tours.models import Product, ProductImage, Category 

# # Create your models here.
# class Cart(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='card')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'carts'
#         verbose_name = 'Cart'
#         verbose_name_plural = 'Carts'

#     def __str__(self):
#         return f"Корзина {self.user.email}"
    
#     @property
#     def total_prise(self):
#         # pass
#         return sum(item.subtotal for item in self.items.all())

#     @property
#     def total_quantity(self):
#         pass
#         # return sum()

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
#     quantity = models.PositiveIntegerField(default=1)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'cart_items'
#         verbose_name = 'Cart Item'
#         verbose_name_plural = 'Cart Items'
#         unique_together = {'cart', 'product'}

#     def __str__(self):
#         return f'{self.product} X {self.quantity}'

#     @property
#     def subtotal(self):
#         return self.product.price * self.quantity