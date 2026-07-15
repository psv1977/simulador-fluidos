from django.urls import path

from simulations.views import hydraulic_simulation, simulation_list


app_name = "simulations"

urlpatterns = [
    path("", hydraulic_simulation, name="hydraulic_simulation"),
    path(
        "mis-simulaciones/",
        simulation_list,
        name="simulation_list",
    ),
]
