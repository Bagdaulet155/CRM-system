from django.contrib.auth.models import User
from django.db import models

class User(models.Model):
    USER_TYPE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.username


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Deal(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    document = models.FileField(upload_to='documents/', null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('new', 'New'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='new')
    
    def str(self):
        return self.title

class Task(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    task_description = models.TextField()
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Task for {self.deal.title}"
