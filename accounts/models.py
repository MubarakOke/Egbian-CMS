from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class MyUserManager(BaseUserManager):
    def create_user(self, username, user_type, position, password=None):

        user = self.model(
            username= username,
            user_type= user_type,   
            position = position 
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username= username,
            user_type= "admin",
            position= "admin",
            password=password,    
        )

        user.is_super_admin = True
        user.save(using=self._db)
        return user

# Create your models here.
class User(AbstractBaseUser):
    username= models.CharField(max_length=255, blank=False, null=False, unique=True)
    user_type= models.CharField(max_length=255, blank=True, null=True)
    position= models.CharField(max_length=255, blank=True, null=True)
    objects = MyUserManager()


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.user_type=='staff'
    
    