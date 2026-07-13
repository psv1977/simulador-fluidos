from django.shortcuts import render

from simulations.calculations import (
    calculate_pipe_area,
    calculate_reynolds_number,
    calculate_velocity,
    classify_flow_regime,
)
from simulations.forms import HydraulicSimulationForm


def hydraulic_simulation(request):
    results = None

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
    else:
        form = HydraulicSimulationForm()

    context = {
        "form": form,
        "results": results,
    }

    return render(
        request,
        "simulations/hydraulic_simulation.html",
        context,
    )
