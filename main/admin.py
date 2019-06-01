from django.contrib import admin

# Register your models here.
from .models import Acc,Parsing

admin.site.register(Acc)
admin.site.register(Parsing)