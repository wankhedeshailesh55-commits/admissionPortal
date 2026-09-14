from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    birth = models.DateField()
    gender = models.CharField(max_length=20)
    course = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name