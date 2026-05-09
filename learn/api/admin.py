from django.contrib import admin

# Register your models here.
from .models import blog,employee
admin.site.register(blog)
admin.site.register(employee)
