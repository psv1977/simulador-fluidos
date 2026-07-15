from decimal import Decimal

from django import forms


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
