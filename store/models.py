from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
class Catagory(models.Model):
    catagory_name=models.CharField(max_length=200,unique=True)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.catagory_name

class Products(models.Model):
    product_name=models.CharField(max_length=200)
    catagory=models.ForeignKey(Catagory,on_delete=models.CASCADE)
    discription=models.CharField(max_length=200)
    price=models.PositiveIntegerField()
    is_active=models.BooleanField(default=True)
    image=models.ImageField(upload_to="images",null=True)
    def __str__(self):
        return self.product_name
    @property
    def offer_price(self):
        off=Offer.objects.filter(product=self)
        if off:
            offs=off[0]
            return self.price-offs.discount
        else:
            return self.price
    @property
    def reviews(self):
        qs=Review.objects.filter(product=self)
        return qs
    @property
    def avg_rating(self):
        qs=self.reviews
        if qs:
            total=sum([r.rating for r in qs])
            return total/len(qs)
        else:
            return 0

class Cart(models.Model):
    products=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    options=(
        ("in-cart","in-cart"),
        ("order-placed","order-placed"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=200,choices=options,default="in-cart")
    quantity=models.PositiveIntegerField(default=1)


class Order(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    address=models.CharField(max_length=200)
    created_date=models.DateField(auto_now_add=True)
    pincode=models.PositiveIntegerField()
    options=(
        ("shipped","shipped"),
        ("order-placed","order-placed"),
        ("in-transit","in-transit"),
        ("delivered","delivered"),
        ("cancelled","cancelled"),
        ("return","return")
    )
    
    status=models.CharField(max_length=30,choices=options,default="order-placed")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    curdate=datetime.date.today()
    eta=curdate+datetime.timedelta(days=5)
    expected_delivery=models.DateField(default=eta)


class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    rating=models.FloatField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self):
        return self.comment

class Offer(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    discount=models.PositiveIntegerField(default=0)
    available=models.BooleanField(default=True)
