from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class MyUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, middle_name, email, user_type, password=None):
        
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            first_name= first_name,
            last_name= last_name,
            middle_name= middle_name,
            email= self.normalize_email(email),
            user_type= user_type    
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            first_name= "",
            last_name= "",
            middle_name= "",
            email= email,
            user_type= "Super Admin",
            password=password,    
        )

        user.is_super_admin = True
        user.save(using=self._db)
        return user

# Create your models here.
class User(AbstractBaseUser):
    first_name= models.CharField(max_length=255, blank=False, null=False)
    last_name= models.CharField(max_length=255, blank=False, null=False)
    middle_name= models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=False,
        blank=False, 
        null=False
    )
    user_type= models.CharField(max_length=255, blank=True, null=True)
    is_super_admin = models.BooleanField(default=False) # a superuser

    objects = MyUserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_super_admin
    
    