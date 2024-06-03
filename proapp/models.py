from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser, Group, Permission

# class User(models.Model):
#     name = models.CharField(max_length=200, null=True)
#     bio = models.TextField(null=True)
#     avatar = models.ImageField(null=True, default="avatar.svg")



class Topic(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
   

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.body[0:30]
    


#### for courses ####

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='product name')
    price = models.IntegerField()
    pdetail = models.CharField(max_length=300, verbose_name='Product detail')
    pimage = models.ImageField(upload_to = 'image')

class Cart(models.Model):
    uid = models.ForeignKey('auth.User',on_delete= models.CASCADE,db_column='uid')
    pid = models.ForeignKey('product',on_delete= models.CASCADE,db_column='pid')
    qty = models.IntegerField(default=1)

class Order(models.Model):
    uid = models.ForeignKey('auth.User',on_delete= models.CASCADE,db_column='uid')
    pid = models.ForeignKey('product',on_delete= models.CASCADE,db_column='pid')
    qty = models.IntegerField(default=1)
    amt = models.IntegerField()

    

# _______  admin  ______
    # use name : rushikesh
    # email  : hrikeshyadav1999@gmail.com
    # password : 9890792387@@
    



