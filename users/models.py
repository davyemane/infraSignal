from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Le numéro de téléphone est requis")
        extra_fields.setdefault('is_superuser', False)  # Explicitly set is_superuser to False
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):  # Inherit from PermissionsMixin
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        # Simplified: Grant all permissions to superuser
        return self.is_superuser

    def has_module_perms(self, app_label):
        # Simplified: Grant access to any app if user is superuser
        return self.is_superuser


class ProblemType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100)  # Pour stocker le nom/chemin de l'icône
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SensitivePoint(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sensitive_points'
    )
    problem_type = models.ForeignKey(
        ProblemType,
        on_delete=models.PROTECT,
        related_name='sensitive_points'
    )
    location = gis_models.PointField()  # Stocke les coordonnées lat/lng
    sector = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'En attente'),
            ('IN_PROGRESS', 'En cours'),
            ('RESOLVED', 'Résolu'),
            ('CANCELED', 'Annulé')
        ],
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.problem_type} - {self.sector}"

class PointImage(models.Model):
    sensitive_point = models.ForeignKey(
        SensitivePoint,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='sensitive_points/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.sensitive_point}"