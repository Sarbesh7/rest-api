from . import views
from django.urls import path

urlpatterns = [
    path('blog/', views.bloglist.as_view(), name='bloglist'),
    path('blog/<int:pk>/', views.blogupdate.as_view(), name='bloglist_update'),
    
    path('employee/', views.EmployeeList.as_view(), name='employeelist'),
    path('employee/<int:pk>/', views.EmployeeDetail.as_view(), name='employeedetail'),
    
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    
]