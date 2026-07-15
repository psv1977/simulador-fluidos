from decimal import Decimal

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
        verbose_name = "curso"
        verbose_name_plural = "cursos"

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
        verbose_name = "inscripción"
        verbose_name_plural = "inscripciones"
        constraints = [
            models.UniqueConstraint(
                fields=["course", "student"],
                name="unique_enrollment_course_student",
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
        verbose_name = "fluido"
        verbose_name_plural = "fluidos"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "reference_temperature_c"],
                name="unique_fluid_temperature_reference",
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} a {self.reference_temperature_c} °C"


class SimulationStatus(models.TextChoices):
    DRAFT = "DRAFT", "Borrador"
    CALCULATED = "CALCULATED", "Calculada"
    INVALID = "INVALID", "Inválida"
    ARCHIVED = "ARCHIVED", "Archivada"


class FlowRegime(models.TextChoices):
    LAMINAR = "LAMINAR", "Laminar"
    TRANSITION = "TRANSITION", "Transicional"
    TURBULENT = "TURBULENT", "Turbulento"


class CalculationModel(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "version"]
        verbose_name = "modelo de cálculo"
        verbose_name_plural = "modelos de cálculo"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} {self.version}"


class Simulation(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="simulations",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        related_name="simulations",
        null=True,
        blank=True,
    )
    fluid = models.ForeignKey(
        Fluid,
        on_delete=models.PROTECT,
        related_name="simulations",
        null=True,
        blank=True,
    )
    calculation_model = models.ForeignKey(
        CalculationModel,
        on_delete=models.PROTECT,
        related_name="simulations",
    )
    title = models.CharField("Título", max_length=150)
    description = models.TextField("Descripción", blank=True)
    status = models.CharField(
        max_length=20,
        choices=SimulationStatus.choices,
        default=SimulationStatus.DRAFT,
    )

    diameter_m = models.DecimalField(
        "Diámetro interno [m]",
        max_digits=12,
        decimal_places=6,
        validators=[MinValueValidator(Decimal("0.000001"))],
    )
    length_m = models.DecimalField(
        "Longitud [m]",
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.0001"))],
    )
    absolute_roughness_m = models.DecimalField(
        "Rugosidad absoluta [m]",
        max_digits=12,
        decimal_places=8,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
    )
    velocity_m_s = models.DecimalField(
        "Velocidad [m/s]",
        max_digits=14,
        decimal_places=8,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.000001"))],
    )
    flow_rate_m3_s = models.DecimalField(
        "Caudal [m³/s]",
        max_digits=14,
        decimal_places=8,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.00000001"))],
    )
    gravity_m_s2 = models.DecimalField(
        "Gravedad [m/s²]",
        max_digits=8,
        decimal_places=5,
        default=Decimal("9.80665"),
        validators=[MinValueValidator(Decimal("0.00001"))],
    )

    density_used_kg_m3 = models.DecimalField(
        "Densidad utilizada [kg/m³]",
        max_digits=10,
        decimal_places=3,
        validators=[MinValueValidator(Decimal("0.001"))],
        editable=False,
    )
    dynamic_viscosity_used_pa_s = models.DecimalField(
        "Viscosidad dinámica utilizada [Pa·s]",
        max_digits=12,
        decimal_places=8,
        validators=[MinValueValidator(Decimal("0.00000001"))],
        editable=False,
    )
    reference_temperature_used_c = models.DecimalField(
        "Temperatura de referencia utilizada [°C]",
        max_digits=6,
        decimal_places=2,
        editable=False,
    )

    area_m2 = models.DecimalField(
        "Área [m²]",
        max_digits=14,
        decimal_places=8,
        null=True,
        blank=True,
    )
    reynolds_number = models.DecimalField(
        "Número de Reynolds",
        max_digits=18,
        decimal_places=6,
        null=True,
        blank=True,
    )
    flow_regime = models.CharField(
        "Régimen de flujo",
        max_length=20,
        choices=FlowRegime.choices,
        null=True,
        blank=True,
    )
    relative_roughness = models.DecimalField(
        "Rugosidad relativa",
        max_digits=14,
        decimal_places=8,
        null=True,
        blank=True,
    )
    friction_factor = models.DecimalField(
        "Factor de fricción",
        max_digits=12,
        decimal_places=8,
        null=True,
        blank=True,
    )
    head_loss_m = models.DecimalField(
        "Pérdida de carga [m]",
        max_digits=14,
        decimal_places=6,
        null=True,
        blank=True,
    )
    pressure_drop_pa = models.DecimalField(
        "Caída de presión [Pa]",
        max_digits=16,
        decimal_places=4,
        null=True,
        blank=True,
    )

    calculation_version = models.CharField(max_length=30, blank=True)
    executed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "simulación"
        verbose_name_plural = "simulaciones"
        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["course"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self) -> str:
        return self.title
