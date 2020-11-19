from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                       PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('User must havee a valid email adress')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Organization(models.Model):
    """Organization that will be able to create projects"""
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    description = models.TextField(blank=True)
    website = models.URLField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CooperatorProfile(models.Model):
    """Profile of a cooperator"""
    name = models.CharField(max_length=255)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    description = models.TextField()
    skills = models.TextField(blank=True)
    website = models.URLField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class PortfolioItem(models.Model):
    """Portfolio items of a cooperator"""
    cooperator = models.ForeignKey(
        CooperatorProfile,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.URLField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    """Cooperation project"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE
    )
    description = models.TextField(blank=True)
    ref_link = models.URLField(max_length=255, blank=True)

    def __str__(self):
        return self.name
