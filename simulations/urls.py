from django.urls import path

from simulations.views import hydraulic_simulation


app_name = "simulations"

urlpatterns = [
    path("", hydraulic_simulation, name="hydraulic_simulation"),
]
