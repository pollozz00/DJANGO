from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])

    def __str__(self):
        return self.name
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', blank=True)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)


    def update_total(self):
        self.total = self.products.aggregate(models.Sum('price'))['price__sum'] or 0.00
        self.save()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_purchased = models.BooleanField(default=False)  # Добавленное поле

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cart.update_total()