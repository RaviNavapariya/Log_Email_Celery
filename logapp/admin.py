from django.contrib import admin
from logapp.models import LogModel, FindindexModel

# Register your models here.

@admin.register(LogModel)
class LogAdmin(admin.ModelAdmin):
    list_display = ['id','type','sub_type', 'shift_name', 'description', 'user']

    
@admin.register(FindindexModel)
class LogAdmin(admin.ModelAdmin):
    list_display = ['id','json_field', 'user']
