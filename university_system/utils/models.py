from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class PhoneNumber(models.Model):
    title = models.CharField(max_length=100)
    number = PhoneNumberField(null=False,blank=False,unique=True)
    internal = models.CharField(max_length=5,null=True,blank=True)
    
    def __str__(self):
        return self.title

class Department(models.Model):
    name = models.CharField(max_length=80)
    phone_number = models.ManyToManyField(PhoneNumber,related_name="department_phone_number")
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    tag = models.CharField(max_length=50)
    url = models.URLField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.tag

class Helper(models.Model):
    help_text = models.CharField(max_length=100)
    url = models.URLField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.help_text
        
class Image(models.Model):
    image = models.ImageField(upload_to="images/")
    date_time = models.DateTimeField(auto_now_add=True)