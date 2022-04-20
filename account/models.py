from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        """Create and save a User with the given phone and password."""
        if not phone:
            raise ValueError("The given phone must be set")
        self.phone = phone
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        """Create and save a regular User with the given phone and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        """Create and save a SuperUser with the given phone and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone, password, **extra_fields)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    """User model."""

    username = None
    email = None
    first_name = None
    last_name = None

    full_name = models.CharField(max_length=160, null=True)
    phone = models.CharField(
        "Phone number",
        unique=True,
        max_length=13,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.full_name)


class BotUser(TimeStampedModel):
    LANG = (
        ("uz", "uz"),
        ("ru", "ru")
    )

    tg_id = models.PositiveBigIntegerField(unique=True, verbose_name="ID")
    full_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Full name")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Phone number")
    is_active = models.BooleanField(default=False, null=True, blank=True, verbose_name="Active")
    lang = models.CharField(max_length=2, choices=LANG, verbose_name="Language")
    is_admin = models.BooleanField(default=False, null=True, blank=True, verbose_name="Admin")
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        if self.phone is not None:
            return str(self.phone)
        return str(self.tg_id)

    class Meta:
        verbose_name = "Bot Customer"
        verbose_name_plural = "Bot Customers"
