from decimal import Decimal
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class HydraulicSimulationForm(forms.Form):
    """Formulario de entrada para una simulación hidráulica básica."""

    title = forms.CharField(
        label="Título de la simulación",
        max_length=150,
        initial="Simulación hidráulica básica",
    )

    diameter_m = forms.DecimalField(
        label="Diámetro interno [m]",
        required=True,
        initial=Decimal("0.1"),
        min_value=Decimal("0.000001"),
        widget=forms.NumberInput(
            attrs={
                "step": "0.001",
                "min": "0.000001",
            }
        ),
    )

    flow_rate_m3_s = forms.DecimalField(
        label="Caudal [m³/s]",
        required=True,
        initial=Decimal("0.01"),
        min_value=Decimal("0.00000001"),
        widget=forms.NumberInput(
            attrs={
                "step": "0.0001",
                "min": "0.00000001",
            }
        ),
    )

    density_kg_m3 = forms.DecimalField(
        label="Densidad [kg/m³]",
        required=True,
        initial=Decimal("1000"),
        min_value=Decimal("0.001"),
        widget=forms.NumberInput(
            attrs={
                "step": "0.001",
                "min": "0.001",
            }
        ),
    )

    dynamic_viscosity_pa_s = forms.DecimalField(
        label="Viscosidad dinámica [Pa·s]",
        required=True,
        initial=Decimal("0.001"),
        min_value=Decimal("0.00000001"),
        widget=forms.NumberInput(
            attrs={
                "step": "0.00000001",
                "min": "0.00000001",
            }
        ),
    )

#creacion de formularios para el registro de usuarios
User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """Formulario para registrar nuevos usuarios en FluidaLab."""

    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
        labels = {
            "username": "Nombre de usuario",
        }

    def clean_email(self):
        """Evita registrar dos usuarios con el mismo correo."""
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Ya existe una cuenta asociada a este correo."
            )

        return email