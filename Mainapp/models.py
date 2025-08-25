from django.db import models
from django.contrib.auth.models import User

class Milkman(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)  # duplicate storage
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    addressline = models.TextField(default=None, null=True, blank=True)
    city = models.CharField(max_length=50, default=None, null=True, blank=True)
    pic = models.URLField(max_length=500,default=None, null=True, blank=True)
    joined=models.DateField(auto_now=True)
    milktype=models.CharField(max_length=20, default="Buffalow")
    price_per_liter=models.IntegerField(default=50)

    def __str__(self):
        return f"{self.id} {self.username}"

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    milkmanuser = models.CharField(max_length=40)
    customeruser = models.CharField(max_length=40)
    value = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating is given by {self.customeruser} for {self.milkmanuser}"

class Costumer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)  # duplicate storage
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    addressline = models.CharField(max_length=100, default=None, null=True, blank=True)
    city = models.CharField(max_length=50, default=None, null=True, blank=True)
    pic = models.URLField(max_length=400, default=None, null=True, blank=True)
    joined=models.DateField(auto_now=True)
    costumer_milkman=models.CharField(max_length=50)
    quantiy_liter=models.DecimalField(max_digits=5, decimal_places=2)
    custumer_request=models.CharField(max_length=30,default="Pending",choices=[("Accept","Acept"),("Reject","Reject"),("Pending","Pending")])

    def __str__(self):
        return f"{self.id} {self.username}"  

class Dairyimages(models.Model):
    id=models.AutoField(primary_key=True)
    milkman_username=models.CharField(max_length=40)
    pic1=models.ImageField(upload_to="dairy",default=None, null=True, blank=True)
    pic2=models.ImageField(upload_to="dairy",default=None, null=True, blank=True)
    pic3=models.ImageField(upload_to="dairy",default=None, null=True, blank=True)
    pic4=models.ImageField(upload_to="dairy",default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.id} {self.milkman_username}"       
class DailyRecord(models.Model):
    date = models.DateField()
    milkman_username = models.CharField(max_length=50)
    customer_username = models.CharField(max_length=50)
    delivered_qty = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    extra_qty = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default="Delivered")
    custumer_status=models.CharField(max_length=30 ,default="Notupdated")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.milkman_username} → {self.customer_username}"

class Discount(models.Model):
    id=models.AutoField(primary_key=True)
    email=models.EmailField()

    def __str__(self):
        return self.email


class Extra_Milk_Today(models.Model):
    id=models.AutoField(primary_key=True)
    date=models.DateField()
    milkman_username =models.CharField(max_length=30)
    milkman_name=models.CharField(max_length=30)
    quantity=models.DecimalField(max_digits=5, decimal_places=2)
    amount=models.IntegerField()
    animal_type = models.CharField(
    max_length=40,
    choices=[
        ("cow", "Cow"),
        ("buffalo", "Buffalo"),
        ("both", "Both")
    ]
    )
    status=models.CharField(max_length=30,choices=[("stock","Stock"),("out of stock","out of stock")],default="stock")
    def __str__(self):
        return  str(self.id) +" "+ self.milkman_name

class Order(models.Model):
    id=models.AutoField(primary_key=True)
    date=models.DateField(auto_now=True)
    buyername=models.CharField(max_length=30)
    username=models.CharField(max_length=30)
    sellerusername=models.CharField(max_length=30)
    sellername=models.CharField(max_length=30)
    price=models.IntegerField()
    pincode=models.IntegerField()
    state=models.CharField(max_length=50)
    delivery_address=models.TextField(blank=True,null=True,default=None)
    payment_mode=models.CharField(max_length=50,choices=[("COD","cash on delivery"),("Online","Online payment")],blank=True,null=True,default=None)
    status=[("pending","pending"),("dispatch","dispatch"),("on the way","on the way"),
            ("out for delivery","out for delivery"),("delivered","delivered"),("cancel","cancel"),("return","return")
            ]
    order_status=models.CharField(max_length=50,choices=status,default="pending")


