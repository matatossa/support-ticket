from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None,role=None):
        if not email :
            raise ValueError('User must have an email address')
      

        user = self.model(
           
            email = self.normalize_email(email),
            role  =role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,  email, password,role):
        if  role not in['client','admin']:
           raise ValueError('erreur du role du client')
        user = self.create_user(
            email = self.normalize_email(email),
            role=role,
            password = password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    role = models.CharField(max_length=10, choices=(('client', 'Client'), ('admin', 'Admin')), default='client')
    Phone_number = models.CharField(max_length=50)

    
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    
    date_joined_for_format = models.DateTimeField(auto_now_add=True)
    last_login_for_format  = models.DateTimeField(auto_now_add=True)
    def date_joined(self):
        return self.date_joined_for_format.strftime('%B %d %Y')
    def last_login(self):
        return self.last_login_for_format.strftime('%B %d %Y')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    objects = AccountManager()

    def __str__(self):
        return self.email
    
    def get_role(self):
     return f'{self.role}'


    # permission
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address = models.TextField(blank=True, max_length=500)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile',default='static/user_image_default.png')
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return self.user.role
