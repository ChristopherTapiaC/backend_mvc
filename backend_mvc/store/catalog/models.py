from django.db import models

class Product (models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    create_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        value = int(self.price)
        price = f"{value:,}".replace(",", ".")
        return f"{self.name} (${price})"

class Client(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return sum(d.quantity * d.product.price for d in self.details.all())

    def __str__(self):
        return f"Venta #{self.pk} - {self.client.name}"

class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
