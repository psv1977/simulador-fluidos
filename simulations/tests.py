"""Pruebas automatizadas para el motor hidráulico de FluidLab."""

from math import pi
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from simulations.calculations import (
    calculate_flow_rate,
    calculate_pipe_area,
    calculate_reynolds_number,
    calculate_velocity,
    classify_flow_regime,
)
from simulations.models import CalculationModel, Simulation, SimulationStatus


class PipeAreaTests(SimpleTestCase):
    """Pruebas para el cálculo del área de una tubería."""

    def test_calculate_pipe_area(self):
        """Debe calcular correctamente el área de una tubería circular."""
        diameter_m = 0.1

        result = calculate_pipe_area(diameter_m)
        expected = pi * (diameter_m / 2) ** 2

        self.assertAlmostEqual(result, expected)

    def test_pipe_area_rejects_zero_diameter(self):
        """Debe rechazar un diámetro igual a cero."""
        with self.assertRaises(ValueError):
            calculate_pipe_area(0)

    def test_pipe_area_rejects_negative_diameter(self):
        """Debe rechazar un diámetro negativo."""
        with self.assertRaises(ValueError):
            calculate_pipe_area(-0.1)


class FlowRateTests(SimpleTestCase):
    """Pruebas para el cálculo del caudal volumétrico."""

    def test_calculate_flow_rate(self):
        """Debe calcular el caudal mediante Q = A × V."""
        result = calculate_flow_rate(
            area_m2=0.01,
            velocity_m_s=2.0,
        )

        self.assertAlmostEqual(result, 0.02)

    def test_flow_rate_rejects_invalid_area(self):
        """Debe rechazar áreas iguales o menores que cero."""
        with self.assertRaises(ValueError):
            calculate_flow_rate(
                area_m2=0,
                velocity_m_s=2.0,
            )

    def test_flow_rate_rejects_invalid_velocity(self):
        """Debe rechazar velocidades iguales o menores que cero."""
        with self.assertRaises(ValueError):
            calculate_flow_rate(
                area_m2=0.01,
                velocity_m_s=0,
            )


class VelocityTests(SimpleTestCase):
    """Pruebas para el cálculo de la velocidad media."""

    def test_calculate_velocity(self):
        """Debe calcular la velocidad mediante V = Q / A."""
        result = calculate_velocity(
            area_m2=0.01,
            flow_rate_m3_s=0.02,
        )

        self.assertAlmostEqual(result, 2.0)

    def test_velocity_rejects_invalid_area(self):
        """Debe rechazar áreas iguales o menores que cero."""
        with self.assertRaises(ValueError):
            calculate_velocity(
                area_m2=0,
                flow_rate_m3_s=0.02,
            )

    def test_velocity_rejects_invalid_flow_rate(self):
        """Debe rechazar caudales iguales o menores que cero."""
        with self.assertRaises(ValueError):
            calculate_velocity(
                area_m2=0.01,
                flow_rate_m3_s=0,
            )


class ReynoldsNumberTests(SimpleTestCase):
    """Pruebas para el cálculo del número de Reynolds."""

    def test_calculate_reynolds_number(self):
        """Debe calcular correctamente el número de Reynolds."""
        result = calculate_reynolds_number(
            density_kg_m3=1000,
            velocity_m_s=2,
            diameter_m=0.1,
            dynamic_viscosity_pa_s=0.001,
        )

        self.assertAlmostEqual(result, 200000)

    def test_reynolds_rejects_invalid_values(self):
        """Debe rechazar parámetros iguales o menores que cero."""
        invalid_cases = [
            {
                "density_kg_m3": 0,
                "velocity_m_s": 2,
                "diameter_m": 0.1,
                "dynamic_viscosity_pa_s": 0.001,
            },
            {
                "density_kg_m3": 1000,
                "velocity_m_s": 0,
                "diameter_m": 0.1,
                "dynamic_viscosity_pa_s": 0.001,
            },
            {
                "density_kg_m3": 1000,
                "velocity_m_s": 2,
                "diameter_m": 0,
                "dynamic_viscosity_pa_s": 0.001,
            },
            {
                "density_kg_m3": 1000,
                "velocity_m_s": 2,
                "diameter_m": 0.1,
                "dynamic_viscosity_pa_s": 0,
            },
        ]

        for parameters in invalid_cases:
            with self.subTest(parameters=parameters):
                with self.assertRaises(ValueError):
                    calculate_reynolds_number(**parameters)


class FlowRegimeTests(SimpleTestCase):
    """Pruebas para la clasificación del régimen de flujo."""

    def test_laminar_flow(self):
        """Debe clasificar como laminar un Reynolds menor que 2300."""
        self.assertEqual(classify_flow_regime(1500), "LAMINAR")

    def test_transition_flow_lower_boundary(self):
        """Reynolds igual a 2300 debe ser transicional."""
        self.assertEqual(classify_flow_regime(2300), "TRANSITION")

    def test_transition_flow(self):
        """Debe clasificar el intervalo transicional."""
        self.assertEqual(classify_flow_regime(3000), "TRANSITION")

    def test_turbulent_flow_lower_boundary(self):
        """Reynolds igual a 4000 debe ser turbulento."""
        self.assertEqual(classify_flow_regime(4000), "TURBULENT")

    def test_turbulent_flow(self):
        """Debe clasificar Reynolds altos como turbulentos."""
        self.assertEqual(classify_flow_regime(100000), "TURBULENT")

    def test_flow_regime_rejects_invalid_reynolds(self):
        """Debe rechazar Reynolds iguales o menores que cero."""
        with self.assertRaises(ValueError):
            classify_flow_regime(0)


class SimulationViewTests(TestCase):
    """Pruebas de autenticación, vistas y persistencia de simulaciones."""

    def setUp(self):
        user_model = get_user_model()
        self.user1 = user_model.objects.create_user(
            username="usuario1",
            password="password-seguro-1",
        )
        self.user2 = user_model.objects.create_user(
            username="usuario2",
            password="password-seguro-2",
        )
        self.calculation_model = CalculationModel.objects.create(
            name="Modelo hidráulico básico",
            version="1.0",
        )
        self.simulation = Simulation.objects.create(
            owner=self.user1,
            calculation_model=self.calculation_model,
            title="Simulación de usuario1",
            status=SimulationStatus.CALCULATED,
            diameter_m=Decimal("0.1"),
            flow_rate_m3_s=Decimal("0.01"),
            density_used_kg_m3=Decimal("1000"),
            dynamic_viscosity_used_pa_s=Decimal("0.001"),
            reference_temperature_used_c=Decimal("20.00"),
            area_m2=Decimal("0.00785398"),
            velocity_m_s=Decimal("1.27323954"),
            reynolds_number=Decimal("127323.954474"),
            flow_regime="TURBULENT",
            calculation_version="1.0",
        )

    def test_simulation_page_requires_login(self):
        response = self.client.get(
            reverse("simulations:hydraulic_simulation")
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_simulation_list_requires_login(self):
        response = self.client.get(reverse("simulations:simulation_list"))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_simulation_detail_requires_login(self):
        response = self.client.get(
            reverse(
                "simulations:simulation_detail",
                args=[self.simulation.pk],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_authenticated_user_can_open_simulation_page(self):
        self.client.login(username="usuario1", password="password-seguro-1")

        response = self.client.get(
            reverse("simulations:hydraulic_simulation")
        )

        self.assertEqual(response.status_code, 200)

    def test_simulation_list_shows_only_owned_simulations(self):
        other_simulation = Simulation.objects.create(
            owner=self.user2,
            calculation_model=self.calculation_model,
            title="Simulación de usuario2",
            status=SimulationStatus.CALCULATED,
            diameter_m=Decimal("0.2"),
            flow_rate_m3_s=Decimal("0.02"),
            density_used_kg_m3=Decimal("1000"),
            dynamic_viscosity_used_pa_s=Decimal("0.001"),
            reference_temperature_used_c=Decimal("20.00"),
            area_m2=Decimal("0.03141593"),
            velocity_m_s=Decimal("0.63661977"),
            reynolds_number=Decimal("127323.954474"),
            flow_regime="TURBULENT",
            calculation_version="1.0",
        )
        self.client.login(username="usuario1", password="password-seguro-1")

        response = self.client.get(reverse("simulations:simulation_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.simulation.title)
        self.assertNotContains(response, other_simulation.title)

    def test_user_can_open_own_simulation_detail(self):
        self.client.login(username="usuario1", password="password-seguro-1")

        response = self.client.get(
            reverse(
                "simulations:simulation_detail",
                args=[self.simulation.pk],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "simulations/simulation_detail.html",
        )

    def test_user_cannot_open_other_users_simulation(self):
        self.client.login(username="usuario2", password="password-seguro-2")

        response = self.client.get(
            reverse(
                "simulations:simulation_detail",
                args=[self.simulation.pk],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_valid_post_creates_simulation(self):
        self.client.login(username="usuario1", password="password-seguro-1")
        initial_count = Simulation.objects.count()

        response = self.client.post(
            reverse("simulations:hydraulic_simulation"),
            {
                "title": "Nueva simulación turbulenta",
                "diameter_m": "0.1",
                "flow_rate_m3_s": "0.01",
                "density_kg_m3": "1000",
                "dynamic_viscosity_pa_s": "0.001",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Simulation.objects.count(), initial_count + 1)

        simulation = Simulation.objects.latest("created_at")
        self.assertEqual(simulation.owner, self.user1)
        self.assertEqual(simulation.status, SimulationStatus.CALCULATED)
        self.assertIsNotNone(simulation.reynolds_number)
        self.assertEqual(simulation.flow_regime, "TURBULENT")
