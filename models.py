

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.conf import settings

CATEGORY_CHOICES =(
    ('Men','Men'),
    ('Women','Women'),
    ('Watch','Watch'),
    ('Bag','Bag'),
    ('Accessories','Accessories')
)

class Item(models.Model):
    title = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=False)
    desc = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True,blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=20,default=None)
    slug = models.SlugField(default="test product")



    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("product",kwargs={
            'slug':self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("add-to-cart",kwargs={
            'slug':self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart",kwargs={
            'slug':self.slug
        })
    @staticmethod
    def get_all_product_by_category(category):
        return Item.objects.filter(category=category)




class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    def get_total_item_price(self):
        return self.quantity * self.item.price
    def get_final_price(self):
        return self.get_total_item_price()
    def get_item_quantity(self):
        return self.quantity


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateField(auto_now_add=True)
    ordered_date = models.DateField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress',on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.user.username
    def get_total(self):
        total= 0
        for i in self.items.all():
            total += i.get_final_price()
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    zip =  models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

