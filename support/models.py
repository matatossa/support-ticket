from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from accounts.models import Account
# Create your models here.
class   Customer(models.Model):
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
class Claim(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('solved', 'Solved'),
    ]
    
    title = models.CharField(max_length=255)
    website_link = models.URLField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    client = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='claims')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='support_users',  
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name=('groups')
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='support_users_permissions',  
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions')
    )
class admin(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)        

from django.contrib.auth import get_user_model

class ArchivedClaim(models.Model):
    client = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    website_link = models.URLField()
    description = models.TextField()
    cause = models.TextField(blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    archived_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField(null=True, blank=True)  # initile bla man implementih 

    def __str__(self):
        return f"Archived Claim: {self.title} by {self.client}"
