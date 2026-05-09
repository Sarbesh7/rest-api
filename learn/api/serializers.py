from rest_framework import serializers
from .models import blog ,employee 
from django.contrib.auth.models import User 


class blogserializer(serializers.ModelSerializer):
    class Meta:
        model=blog
        fields='__all__'


class employeeserializer(serializers.ModelSerializer):
    class Meta:
        model=employee
        fields='name','email','phone'

class Loginserializer(serializers.Serializer):
    username=serializers.CharField(max_length=100)
    password=serializers.CharField(max_length=100)
    
    
    
    
    
class Registerserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username','email','password')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user