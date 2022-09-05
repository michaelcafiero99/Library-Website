"""
Definition of models.
"""

from django.db import models

# Create your models here.
class Customers(models.Model):
    userName = models.TextField(max_length = 255)
    password = models.TextField(max_length = 255)
    firstName = models.TextField(max_length = 255)
    lastName = models.TextField(max_length = 255)
    emailAddress = models.TextField(max_length = 255, null=True)

class Items(models.Model):
    itemType = models.TextField(max_length = 255)
    itemName = models.TextField(max_length = 255)
    author = models.TextField(max_length = 255)
    itemsLeft = models.IntegerField()
    rentedCount = models.IntegerField()

class Rooms(models.Model):
    renterId = models.ForeignKey('Customers', on_delete = models.CASCADE)
    currState = models.TextField(max_length = 10)
    
class Employees(models.Model):
    userName = models.TextField(max_length = 255)
    password = models.TextField(max_length = 255)
    firstName = models.TextField(max_length = 255)
    lastName = models.TextField(max_length = 255)
    emailAddress = models.TextField(max_length = 255, null=True)

class RentedBooks(models.Model):
    renterId = models.ForeignKey('Customers', on_delete = models.CASCADE)
    itemId = models.ForeignKey('Items', on_delete = models.CASCADE)
