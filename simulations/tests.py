from math import pi

from django.test import SimpleTestCase

from simulations.calculations import (
    calculate_flow_rate,
    calculate_pipe_area,
    calculate_reynolds_number,
    calculate_velocity,
    classify_flow_regime,
)


class HydraulicCalculationsTests(SimpleTestCase):
    """Unit tests for hydraulic calculation helpers."""

    def test_calculate_pipe_area_with_valid_diameter(self):
        area_m2 = calculate_pipe_area(2.0)

        self.assertAlmostEqual(area_m2, pi)

    def test_calculate_pipe_area_with_small_positive_diameter(self):
        area_m2 = calculate_pipe_area(0.001)

        self.assertAlmostEqual(area_m2, pi * (0.0005**2))

    def test_calculate_pipe_area_rejects_zero_diameter(self):
        with self.assertRaises(ValueError):
            calculate_pipe_area(0)

    def test_calculate_pipe_area_rejects_negative_diameter(self):
        with self.assertRaises(ValueError):
            calculate_pipe_area(-0.1)

    def test_calculate_flow_rate_with_valid_inputs(self):
        flow_rate_m3_s = calculate_flow_rate(area_m2=0.5, velocity_m_s=2.0)

        self.assertAlmostEqual(flow_rate_m3_s, 1.0)

    def test_calculate_flow_rate_with_small_positive_inputs(self):
        flow_rate_m3_s = calculate_flow_rate(
            area_m2=0.0001,
            velocity_m_s=0.001,
        )

        self.assertAlmostEqual(flow_rate_m3_s, 0.0000001)

    def test_calculate_flow_rate_rejects_zero_area(self):
        with self.assertRaises(ValueError):
            calculate_flow_rate(area_m2=0, velocity_m_s=2.0)

    def test_calculate_flow_rate_rejects_zero_velocity(self):
        with self.assertRaises(ValueError):
            calculate_flow_rate(area_m2=0.5, velocity_m_s=0)

    def test_calculate_flow_rate_rejects_negative_area(self):
        with self.assertRaises(ValueError):
            calculate_flow_rate(area_m2=-0.5, velocity_m_s=2.0)

    def test_calculate_flow_rate_rejects_negative_velocity(self):
        with self.assertRaises(ValueError):
            calculate_flow_rate(area_m2=0.5, velocity_m_s=-2.0)

    def test_calculate_velocity_with_valid_inputs(self):
        velocity_m_s = calculate_velocity(area_m2=0.5, flow_rate_m3_s=1.0)

        self.assertAlmostEqual(velocity_m_s, 2.0)

    def test_calculate_velocity_with_small_positive_inputs(self):
        velocity_m_s = calculate_velocity(
            area_m2=0.0001,
            flow_rate_m3_s=0.0000001,
        )

        self.assertAlmostEqual(velocity_m_s, 0.001)

    def test_calculate_velocity_rejects_zero_area(self):
        with self.assertRaises(ValueError):
            calculate_velocity(area_m2=0, flow_rate_m3_s=1.0)

    def test_calculate_velocity_rejects_zero_flow_rate(self):
        with self.assertRaises(ValueError):
            calculate_velocity(area_m2=0.5, flow_rate_m3_s=0)

    def test_calculate_velocity_rejects_negative_area(self):
        with self.assertRaises(ValueError):
            calculate_velocity(area_m2=-0.5, flow_rate_m3_s=1.0)

    def test_calculate_velocity_rejects_negative_flow_rate(self):
        with self.assertRaises(ValueError):
            calculate_velocity(area_m2=0.5, flow_rate_m3_s=-1.0)

    def test_calculate_reynolds_number_with_valid_inputs(self):
        reynolds_number = calculate_reynolds_number(
            density_kg_m3=1000,
            velocity_m_s=2,
            diameter_m=0.05,
            dynamic_viscosity_pa_s=0.001,
        )

        self.assertAlmostEqual(reynolds_number, 100000)

    def test_calculate_reynolds_number_with_boundary_like_laminar_value(self):
        reynolds_number = calculate_reynolds_number(
            density_kg_m3=1000,
            velocity_m_s=0.02299,
            diameter_m=0.1,
            dynamic_viscosity_pa_s=0.001,
        )

        self.assertAlmostEqual(reynolds_number, 2299)

    def test_calculate_reynolds_number_rejects_zero_values(self):
        invalid_inputs = (
            {
                "density_kg_m3": 0,
                "velocity_m_s": 1,
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
                "velocity_m_s": 1,
                "diameter_m": 0,
                "dynamic_viscosity_pa_s": 0.001,
            },
            {
                "density_kg_m3": 1000,
                "velocity_m_s": 1,
                "diameter_m": 0.1,
                "dynamic_viscosity_pa_s": 0,
            },
        )

        for values in invalid_inputs:
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    calculate_reynolds_number(**values)

    def test_calculate_reynolds_number_rejects_negative_values(self):
        valid_inputs = {
            "density_kg_m3": 1000,
            "velocity_m_s": 1,
            "diameter_m": 0.1,
            "dynamic_viscosity_pa_s": 0.001,
        }

        for field_name in valid_inputs:
            values = valid_inputs.copy()
            values[field_name] = -values[field_name]

            with self.subTest(field_name=field_name):
                with self.assertRaises(ValueError):
                    calculate_reynolds_number(**values)

    def test_classify_flow_regime_valid_ranges(self):
        cases = (
            (1, "LAMINAR"),
            (1500, "LAMINAR"),
            (2500, "TRANSITION"),
            (5000, "TURBULENT"),
        )

        for reynolds_number, expected_regime in cases:
            with self.subTest(reynolds_number=reynolds_number):
                self.assertEqual(
                    classify_flow_regime(reynolds_number),
                    expected_regime,
                )

    def test_classify_flow_regime_reynolds_limits(self):
        cases = (
            (2299, "LAMINAR"),
            (2300, "TRANSITION"),
            (3999, "TRANSITION"),
            (4000, "TURBULENT"),
        )

        for reynolds_number, expected_regime in cases:
            with self.subTest(reynolds_number=reynolds_number):
                self.assertEqual(
                    classify_flow_regime(reynolds_number),
                    expected_regime,
                )

    def test_classify_flow_regime_rejects_zero_reynolds_number(self):
        with self.assertRaises(ValueError):
            classify_flow_regime(0)

    def test_classify_flow_regime_rejects_negative_reynolds_number(self):
        with self.assertRaises(ValueError):
            classify_flow_regime(-1)
