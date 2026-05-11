from django.shortcuts import render
from rest_framework import generics
from .models import blog,employee
from .serializers import blogserializer ,employeeserializer , Loginserializer , Registerserializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page  #for caching the login response for 2 minutes





Group.objects.get_or_create(name='Boss')
Group.objects.get_or_create(name='Employee')


class IsBoss(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name='Boss').exists()
        )
class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name='Employee').exists()
        )


# Create your views here.
class bloglist(generics.ListCreateAPIView):
   queryset=blog.objects.all()
   serializer_class=blogserializer
   
class blogupdate(generics.RetrieveUpdateDestroyAPIView):
    queryset=blog.objects.all()
    serializer_class=blogserializer
    lookup_field="pk"
    

class EmployeeList(APIView):
    permission_classes = [IsBoss]
   

    def get(self, request):
        employees = employee.objects.all()
        serializer = employeeserializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = employeeserializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        emp = employee.objects.get(pk=pk)
        emp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        emp = employee.objects.get(pk=pk)

        serializer = employeeserializer(emp, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   
class EmployeeDetail(APIView):
    
    permission_classes = [IsEmployee]
    
    def get(self, request, pk):
      try:
         emp = employee.objects.get(pk=pk)
         serializer = employeeserializer(emp)
         return Response(serializer.data, status=status.HTTP_200_OK)
      except employee.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
   
    def put(self, request, pk):
      try:
         employee_instance=employee.objects.get(pk=pk)
      except employee.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
      serializer=employeeserializer(employee_instance, data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_200_OK)
      


class RegisterAPI(APIView):
    def post(self,request):
        data=request.data
        serializer=Registerserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginAPI(APIView):
    @method_decorator(cache_page(60*2)) #cachee for 2 minutes
    
    def post(self,request):
        data=request.data
        serializer=Loginserializer(data=data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        username=serializer.validated_data['username']
        password=serializer.validated_data['password']
        
        user_object=authenticate(username=username, password=password)
        if user_object:
            token, _ = Token.objects.get_or_create(user=user_object)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        