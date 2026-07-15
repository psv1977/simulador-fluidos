"""Pruebas automatizadas para el motor hidráulico de FluidLab."""

from math import pi

from django.test import SimpleTestCase

from simulations.calculations import (
    calculate_flow_rate,
    calculate_pipe_area,
    calculate_reynolds_number,
    calculate_velocity,
    classify_flow_regime,
)


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