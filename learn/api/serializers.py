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
    #write_only=True means that the password field will not be included in the serialized output when retrieving user data, but it will be required when creating a new user.
    
    password=serializers.CharField(write_only=True)
    
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
    
    

#nested serializer for showing the teacher name in the course details
class teacherserializer(serializers.ModelSerializer):
    class Meta:
        model=employee
        fields='name'
        
class courseserializer(serializers.ModelSerializer):
    teacher=teacherserializer()
    class Meta:
        model=blog
        fields='__all__'   