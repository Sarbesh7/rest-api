from django.db import models

# Create your models here.
class blog(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    age=models.IntegerField()
    
    
    def __str__(self):
        return self.title
    
    
class employee(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=20)
    
    def __str__(self):
        return self.name   
    
  