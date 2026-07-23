"""Cálculos hidráulicos básicos para FluidLab.

Todas las funciones utilizan unidades del Sistema Internacional.
Este módulo no depende de Django.
"""

from math import pi


def calculate_pipe_area(diameter_m: float) -> float:
    """Calcula el área transversal de una tubería circular.

    Args:
        diameter_m: Diámetro interno de la tubería, en metros.

    Returns:
        Área transversal, en metros cuadrados.

    Raises:
        ValueError: Si el diámetro no es mayor que cero.
    """
    if diameter_m <= 0:
        raise ValueError("El diámetro debe ser mayor que cero.")

    radius_m = diameter_m / 2
    return pi * radius_m**2


def calculate_flow_rate(area_m2: float, velocity_m_s: float) -> float:
    """Calcula el caudal volumétrico a partir del área y la velocidad.

    Q = A × V

    Args:
        area_m2: Área transversal, en metros cuadrados.
        velocity_m_s: Velocidad media del fluido, en metros por segundo.

    Returns:
        Caudal volumétrico, en metros cúbicos por segundo.

    Raises:
        ValueError: Si el área o la velocidad no son mayores que cero.
    """
    if area_m2 <= 0:
        raise ValueError("El área debe ser mayor que cero.")

    if velocity_m_s <= 0:
        raise ValueError("La velocidad debe ser mayor que cero.")

    return area_m2 * velocity_m_s


def calculate_velocity(area_m2: float, flow_rate_m3_s: float) -> float:
    """Calcula la velocidad media a partir del área y el caudal.

    V = Q / A

    Args:
        area_m2: Área transversal, en metros cuadrados.
        flow_rate_m3_s: Caudal volumétrico, en metros cúbicos por segundo.

    Returns:
        Velocidad media, en metros por segundo.

    Raises:
        ValueError: Si el área o el caudal no son mayores que cero.
    """
    if area_m2 <= 0:
        raise ValueError("El área debe ser mayor que cero.")

    if flow_rate_m3_s <= 0:
        raise ValueError("El caudal debe ser mayor que cero.")

    return flow_rate_m3_s / area_m2


def calculate_reynolds_number(
    density_kg_m3: float,
    velocity_m_s: float,
    diameter_m: float,
    dynamic_viscosity_pa_s: float,
) -> float:
    """Calcula el número de Reynolds para flujo interno en tuberías.

    Re = (ρ × V × D) / μ

    Args:
        density_kg_m3: Densidad del fluido, en kg/m³.
        velocity_m_s: Velocidad media, en m/s.
        diameter_m: Diámetro interno, en m.
        dynamic_viscosity_pa_s: Viscosidad dinámica, en Pa·s.

    Returns:
        Número de Reynolds, adimensional.

    Raises:
        ValueError: Si algún parámetro no es mayor que cero.
    """
    values = {
        "La densidad": density_kg_m3,
        "La velocidad": velocity_m_s,
        "El diámetro": diameter_m,
        "La viscosidad dinámica": dynamic_viscosity_pa_s,
    }

    for field_name, value in values.items():
        if value <= 0:
            raise ValueError(f"{field_name} debe ser mayor que cero.")

    return (
        density_kg_m3
        * velocity_m_s
        * diameter_m
        / dynamic_viscosity_pa_s
    )


def classify_flow_regime(reynolds_number: float) -> str:
    """Clasifica el régimen de flujo según el número de Reynolds.

    Criterio inicial para flujo interno en tuberías:

    - Re < 2300: laminar.
    - 2300 ≤ Re < 4000: transicional.
    - Re ≥ 4000: turbulento.

    Args:
        reynolds_number: Número de Reynolds, adimensional.

    Returns:
        Régimen de flujo: ``LAMINAR``, ``TRANSITION`` o ``TURBULENT``.

    Raises:
        ValueError: Si Reynolds no es mayor que cero.
    """
    if reynolds_number <= 0:
        raise ValueError("El número de Reynolds debe ser mayor que cero.")

    if reynolds_number < 2300:
        return "LAMINAR"

    if reynolds_number < 4000:
        return "TRANSITION"

    return "TURBULENT"