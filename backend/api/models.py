from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, user_type, password, **kwargs):
        if not email:
            raise ValueError("The email must be set")
        if not password:
            raise ValueError("The password must be set")
        if not user_type:
            raise ValueError("The user_type must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, password=password, **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, user_type, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        if kwargs.get("is_staff") is not True:
            raise ValueError(("Superuser must have is_staff=True."))
        if kwargs.get("is_superuser") is not True:
            raise ValueError(("Superuser must have is_superuser=True."))
        return self.create_user(email, user_type, password, **kwargs)

class MyUser(AbstractUser):
    class UserTypes(models.TextChoices):
        EMPLOYEE = "employee"
        ANALYST = "analyst"
        DEPARTMENT_DIR = "department_dir"
        ADMIN = "admin"
    email = models.EmailField(max_length=254, unique=True, verbose_name="E-mail пользователя")
    user_type = models.CharField(max_length=20, choices=UserTypes.choices, default=UserTypes.EMPLOYEE)
    username = None
    department = models.ManyToManyField("Department")
    USERNAME_FIELD="email"

    REQUIRED_FIELDS = ["password", "user_type"]
    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Department(models.Model):
    address = models.TextField(verbose_name="Адрес отделения", default="")
    contact = models.ForeignKey("Phone", on_delete=models.SET_NULL, null=True, to_field="id")
    post_index = models.CharField(max_length=6, unique=False, null=False, verbose_name="Почтвый индекс", default="")

    def __str__(self):
        return self.address

class Employee(models.Model):
    user = models.ForeignKey("MyUser", on_delete=models.CASCADE, null=True, to_field='id')
    expirience = models.IntegerField(verbose_name="Стаж работы")
    salary = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Оклад")
    contact = models.ForeignKey("Phone", on_delete=models.SET_NULL, null=True, to_field="id")
    rank = models.CharField(max_length=30, unique=False, null=True, verbose_name="Звание", default="")
    information = models.TextField(verbose_name="Информация о сотруднике")

    def __str__(self):
        return self.user.email

class Migrant(models.Model):
    class Status(models.TextChoices):
        ok="registered"
        ntok = "unregistered"
    name = models.TextField(verbose_name="ФИО", null=False, unique=False, default="")
    address = models.TextField(verbose_name="Адрес проживания")
    birthday = models.DateField(unique=False, null=False, verbose_name="Дата рождения", default="")
    birthday_place = models.TextField(verbose_name="Место рождения")
    citizenship = models.ForeignKey("Citizenship", on_delete=models.SET_NULL, null=True, verbose_name="Гражданство", to_field="id")
    profession = models.CharField(max_length=150, unique=False, null=False, verbose_name="Профессия", default="Безработный")
    contact = models.ForeignKey("Phone", on_delete=models.SET_NULL, null=True, to_field="id")
    document = models.ForeignKey("Doc_migr_pers", on_delete=models.SET_NULL, null=True, to_field="id")
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.ntok)

    def __str__(self):
        return self.name

class Phone(models.Model):
    number = models.CharField(max_length=11, unique=True, null=False, blank=True, verbose_name="Номер телефона")

    def __str__(self):
        return self.number

class Doc_migr_pers(models.Model):
    serial_number = models.CharField(max_length=20, null=False, unique=True, verbose_name="Серия и номер документа", default="")
    issued_by = models.TextField(verbose_name="Кем выдан документ", default="")
    # добавить тип документа
    issued_when = models.DateField(unique=False, null=False, verbose_name="Дата выдачи документа", default="")
    expires_when = models.DateField(unique=False, null=True, verbose_name="Дата окончания срока действия документа", default="")

    def __str__(self):
        return self.serial_number

class Citizenship(models.Model):
    class OKIN(models.TextChoices):
        russia = "1"
        double = "2"
        inostr = "3"
        without = "4"
    code = models.CharField(max_length=1, choices=OKIN.choices, default=OKIN.without)
    name = models.CharField(max_length = 50, unique=True, null=False, verbose_name="Название страны", default = "")

    def __str__(self):
        return self.name

class Registration_Statement(models.Model):
    class Status(models.TextChoices):
        first="pending"
        second="approval"
        third="approved"
        declined="declined"
    department = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True, to_field='id')
    person = models.ForeignKey("Migrant", on_delete=models.SET_NULL, null=True, to_field='id')
    date = models.DateField(unique=False, null=False, verbose_name="Дата заполнения документа", default="")
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.first)

class Unregistration_Statement(models.Model):
    class Status(models.TextChoices):
        first="pending"
        second="approval"
        third="approved"
        declined="declined"
    department = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True, to_field="id")
    person = models.ForeignKey("Migrant", on_delete=models.SET_NULL, null=True, to_field="id")
    date = models.DateField(unique=False, null=False, verbose_name="Дата заполнения документа", default="")
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.first)





