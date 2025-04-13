from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El Email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    int_idUser = models.AutoField(primary_key=True)
    str_email = models.EmailField(unique=True)
    str_username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    bool_activo = models.BooleanField(default=True)

    USERNAME_FIELD = 'str_email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.str_email

class Docente(models.Model):
    str_idDocente = models.CharField(primary_key=True, max_length=20)  # Ejemplo: "D001", "D002"
    int_idUser = models.OneToOneField(User, on_delete=models.CASCADE, related_name='docente', to_field='int_idUser')
    str_nombres = models.CharField(max_length=100)
    str_apellidos = models.CharField(max_length=100)
    str_especialidad = models.CharField(max_length=100, blank=True, null=True)
    bool_activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.str_idDocente} - {self.str_nombres} {self.str_apellidos}"

    class Meta:
        db_table = 'docente'
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'

class Alumno(models.Model):
    str_idAlumno = models.CharField(primary_key=True, max_length=20)  # Ejemplo: "A001", "A002"
    int_idUser = models.OneToOneField(User, on_delete=models.CASCADE, related_name='alumno', to_field='int_idUser')
    str_nombres = models.CharField(max_length=100)
    str_apellidos = models.CharField(max_length=100)
    dt_fecha_nacimiento = models.DateField(blank=True, null=True)
    bool_activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.str_idAlumno} - {self.str_nombres} {self.str_apellidos}"

    class Meta:
        db_table = 'alumno'
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
