from django.db import models
from django.contrib.auth.models import User

class LogModel(models.Model):
    type = models.CharField(max_length=30)
    sub_type = models.CharField(max_length=30)
    shift_name = models.CharField(max_length=30)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.type

class FindindexModel(models.Model):
    json_field = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)