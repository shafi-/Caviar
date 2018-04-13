from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Customer(models.Model):
    pending = 'Pending'
    verified = 'Verified'

    STATUS = (
        (pending,pending),
        (verified,verified),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    contact = models.CharField(max_length = 10)
    orders = models.IntegerField(default=0)
    total_sale = models.IntegerField(default=0)

    def __str__(self):
        return self.customer.first_name + " " + self.customer.last_name

class Staff(models.Model):
    admin = 'Admin'
    deliveryboy = 'Delivery Boy'
    chef = 'Chef'

    ROLES = (
        (admin,admin),
        (chef,chef),
        (deliveryboy,deliveryboy),
    )
    
    staff_id = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = User.first_name
    last_name = User.last_name
    address = models.TextField()
    contact = models.CharField(max_length = 10)
    email = User.email
    salary = models.IntegerField()
    role = models.CharField(max_length = 30, choices = ROLES)
    
    def __str__(self):
        return self.first_name + " " + self.last_name

class Order(models.Model):
    pending = 'Pending'
    completed = 'Completed'

    STATUS = (
        (pending,pending),
        (completed,completed),
    )

    cod = 'Cash On Delivery'
    card = 'Card Payment'
    upi = 'UPI Payment'

    PAYMENT = (
        (cod,cod),
        (card,card),
        (upi,upi),
    )

    pickup = 'PickUp'
    delivery = 'Delivery'

    TYPE = (
        (pickup, pickup),
        (delivery, delivery),
    )
    
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_timestamp = models.DateTimeField(blank=True)
    delivery_timestamp = models.DateTimeField(blank=True)
    payment_status = models.CharField(max_length = 30, choices = STATUS)
    delivery_status = models.CharField(max_length = 30, choices = STATUS)
    if_cancelled = models.BooleanField(default = False)
    total_amount = models.IntegerField()
    payment_method = models.CharField(max_length = 30, choices = PAYMENT)
    location = models.CharField(max_length=200, blank=True, null=True)

    def confirmOrder(self):
        self.order_timestamp = timezone.now()
        self.payment_status = self.completed
        self.save()

    def confirmDelivery(self):
        self.delivery_timestamp = timezone.now()
        self.delivery_status = self.completed
        self.save()
    
    def __str__(self):
        return self.customer.first_name + " " + self.customer.last_name

class Food(models.Model):
    indian = 'Indian'
    chinese = 'Chinese'
    continental = 'Continental'
    
    COURSE = (
        (indian,indian),
        (chinese,chinese),
        (continental,continental),
    )

    disabled = 'Disabled'
    enabled = 'Enabled'

    STATUS = (
        (disabled, disabled),
        (enabled, enabled),
    )

    #food_id
    name = models.CharField(max_length=250)
    course = models.CharField(max_length = 50, choices = COURSE)
    status = models.CharField(max_length=50, choices=STATUS)
    content_description = models.TextField()
    base_price = models.FloatField()
    discount = models.DecimalField(default=0, decimal_places=2, max_digits=5)
    
    #sale_price = (100.0 - float(discount))/100.0 * float(base_price)

class Comment(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)