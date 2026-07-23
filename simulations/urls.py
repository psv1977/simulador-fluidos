from django.urls import path

from simulations.views import (
    hydraulic_simulation,
    simulation_detail,
    simulation_list,
)


app_name = "simulations"

urlpatterns = [
    path("", hydraulic_simulation, name="hydraulic_simulation"),
    path(
        "mis-simulaciones/",
        simulation_list,
        name="simulation_list",
    ),
    path(
        "mis-simulaciones/<int:pk>/",
        simulation_detail,
        name="simulation_detail",
    ),
]
