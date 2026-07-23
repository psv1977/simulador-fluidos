from django.contrib import admin

from .models import (
    CalculationModel,
    Course,
    Enrollment,
    Fluid,
    Profile,
    Simulation,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "academic_id", "institution")
    list_filter = ("role", "institution")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "academic_id",
        "institution",
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "professor",
        "academic_year",
        "semester",
        "is_active",
    )
    list_filter = ("academic_year", "semester", "is_active")
    search_fields = (
        "code",
        "name",
        "professor__username",
        "professor__first_name",
        "professor__last_name",
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "status", "enrolled_at")
    list_filter = ("status", "course")
    search_fields = (
        "student__username",
        "student__first_name",
        "student__last_name",
        "course__code",
        "course__name",
    )


@admin.register(Fluid)
class FluidAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "density_kg_m3",
        "dynamic_viscosity_pa_s",
        "reference_temperature_c",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name", "reference_temperature_c")


@admin.register(CalculationModel)
class CalculationModelAdmin(admin.ModelAdmin):
    list_display = ("name", "version", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "version")
    ordering = ("name", "version")


@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "course",
        "fluid",
        "calculation_model",
        "status",
        "created_at",
        "executed_at",
    )
    list_filter = (
        "status",
        "course",
        "fluid",
        "calculation_model",
        "created_at",
    )
    search_fields = (
        "title",
        "description",
        "owner__username",
        "owner__first_name",
        "owner__last_name",
        "course__code",
        "course__name",
    )
    readonly_fields = (
        "density_used_kg_m3",
        "dynamic_viscosity_used_pa_s",
        "reference_temperature_used_c",
        "created_at",
        "updated_at",
    )
    date_hierarchy = "created_at"
    ordering = ("-created_at",)