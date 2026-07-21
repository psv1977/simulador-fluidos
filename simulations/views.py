from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from simulations.calculations import (
    calculate_pipe_area,
    calculate_reynolds_number,
    calculate_velocity,
    classify_flow_regime,
)
from simulations.forms import HydraulicSimulationForm
from simulations.models import CalculationModel, Simulation, SimulationStatus


@login_required
def simulation_list(request):
    simulations = (
        Simulation.objects.filter(owner=request.user)
        .select_related(
            "calculation_model",
            "fluid",
            "course",
        )
    )

    return render(
        request,
        "simulations/simulation_list.html",
        {"simulations": simulations},
    )


@login_required
def simulation_detail(request, pk):
    simulation = get_object_or_404(
        Simulation.objects.select_related(
            "calculation_model",
            "fluid",
            "course",
        ),
        pk=pk,
        owner=request.user,
    )

    return render(
        request,
        "simulations/simulation_detail.html",
        {"simulation": simulation},
    )


@login_required
def hydraulic_simulation(request):
    results = None
    saved_simulation = None

    if request.method == "POST":
        form = HydraulicSimulationForm(request.POST)

        if form.is_valid():
            diameter_m = float(form.cleaned_data["diameter_m"])
            flow_rate_m3_s = float(form.cleaned_data["flow_rate_m3_s"])
            density_kg_m3 = float(form.cleaned_data["density_kg_m3"])
            dynamic_viscosity_pa_s = float(
                form.cleaned_data["dynamic_viscosity_pa_s"]
            )

            area_m2 = calculate_pipe_area(
                diameter_m=diameter_m,
            )

            velocity_m_s = calculate_velocity(
                area_m2=area_m2,
                flow_rate_m3_s=flow_rate_m3_s,
            )

            reynolds_number = calculate_reynolds_number(
                density_kg_m3=density_kg_m3,
                velocity_m_s=velocity_m_s,
                diameter_m=diameter_m,
                dynamic_viscosity_pa_s=dynamic_viscosity_pa_s,
            )

            flow_regime = classify_flow_regime(reynolds_number)

            results = {
                "area_m2": area_m2,
                "velocity_m_s": velocity_m_s,
                "reynolds_number": reynolds_number,
                "flow_regime": flow_regime,
            }

            calculation_model, _ = CalculationModel.objects.get_or_create(
                name="Modelo hidráulico básico",
                version="1.0",
                defaults={
                    "description": (
                        "Calcula área, velocidad, número de Reynolds "
                        "y régimen de flujo."
                    ),
                    "is_active": True,
                },
            )

            saved_simulation = Simulation.objects.create(
                owner=request.user,
                calculation_model=calculation_model,
                title=form.cleaned_data["title"],
                status=SimulationStatus.CALCULATED,
                diameter_m=form.cleaned_data["diameter_m"],
                flow_rate_m3_s=form.cleaned_data["flow_rate_m3_s"],
                density_used_kg_m3=form.cleaned_data["density_kg_m3"],
                dynamic_viscosity_used_pa_s=(
                    form.cleaned_data["dynamic_viscosity_pa_s"]
                ),
                reference_temperature_used_c=Decimal("20.00"),
                area_m2=Decimal(str(area_m2)),
                velocity_m_s=Decimal(str(velocity_m_s)),
                reynolds_number=Decimal(str(reynolds_number)),
                flow_regime=flow_regime,
                calculation_version="1.0",
                executed_at=timezone.now(),
            )

    else:
        form = HydraulicSimulationForm()

    context = {
        "form": form,
        "results": results,
        "saved_simulation": saved_simulation,
    }

    return render(
        request,
        "simulations/hydraulic_simulation.html",
        context,
    )
