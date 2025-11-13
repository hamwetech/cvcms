from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from conf.models import District, County, SubCounty, Parish

class AccessLevel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# ----------------------------
# Custom User Manager
# ----------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user"""
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)


# ----------------------------
# Custom User Model
# ----------------------------
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    profile_photo = models.ImageField(upload_to='user/', null=True, blank=True)
    sex = models.CharField('Sex', max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')), null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    msisdn = models.CharField(max_length=12, unique=True, null=True, blank=True)
    nin = models.CharField(max_length=255, null=True, blank=True)
    access_level = models.ForeignKey(AccessLevel, null=True, blank=True, on_delete=models.CASCADE)
    district = models.ForeignKey("conf.District", null=True, blank=True, on_delete=models.SET_NULL, related_name="profile_district")
    county = models.ForeignKey("conf.County", null=True, blank=True, on_delete=models.SET_NULL)
    sub_county = models.ForeignKey("conf.SubCounty", null=True, blank=True, on_delete=models.SET_NULL)
    parish = models.ForeignKey("conf.Parish", null=True, blank=True, on_delete=models.SET_NULL)
    village = models.CharField(max_length=150, null=True, blank=True)
    gps_coodinates = models.CharField(max_length=150, null=True, blank=True)
    district_incharge = models.ManyToManyField("conf.District", blank=True)
    is_supervisor = models.BooleanField(default=False)
    supervisor = models.ForeignKey('self', null=True, blank=True, related_name="supervisees", on_delete=models.SET_NULL)
    is_locked = models.BooleanField(default=False)
    receive_sms_notifications = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    otp_secret = models.CharField(max_length=32, blank=True, null=True)

    # Django system fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
