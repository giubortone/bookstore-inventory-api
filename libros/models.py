from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=120)
    isbn = models.CharField(max_length=13, unique=True)
    cost_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_price_local = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100, default="General")   
    supplier_country = models.CharField(max_length=2, default="US")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.author}"
