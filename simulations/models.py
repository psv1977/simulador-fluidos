from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Profile(models.Model):
    class Role(models.TextChoices):
        PROFESSOR = "PROFESSOR", "Profesor"
        STUDENT = "STUDENT", "Alumno"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )
    academic_id = models.CharField(
        max_length=50,
        blank=True,
    )
    institution = models.CharField(
        max_length=150,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.get_role_display()}"


class Course(models.Model):
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="courses_taught",
    )
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    academic_year = models.PositiveIntegerField()
    semester = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-academic_year", "code"]

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class Enrollment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Activa"
        COMPLETED = "COMPLETED", "Finalizada"
        WITHDRAWN = "WITHDRAWN", "Retirada"

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_enrollments",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "student"],
                name="unique_student_course_enrollment",
            )
        ]

    def __str__(self) -> str:
        return f"{self.student.username} en {self.course.code}"


class Fluid(models.Model):
    name = models.CharField(max_length=100)
    density_kg_m3 = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        validators=[MinValueValidator(0.001)],
    )
    dynamic_viscosity_pa_s = models.DecimalField(
        max_digits=12,
        decimal_places=8,
        validators=[MinValueValidator(0.00000001)],
    )
    reference_temperature_c = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "reference_temperature_c"],
                name="unique_fluid_temperature_reference",
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} a {self.reference_temperature_c} °C"