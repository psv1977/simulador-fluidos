# FluidLab

## Descripción

FluidLab es una plataforma web educativa desarrollada en Python y Django para apoyar la enseñanza y simulación de fenómenos asociados a la Mecánica de Fluidos.

La primera versión estará enfocada en el análisis de flujo en tuberías, permitiendo modificar variables hidráulicas, ejecutar simulaciones, almacenar resultados en una base de datos PostgreSQL y consultar el historial de uso de cada usuario.

## Objetivo general

Desarrollar una aplicación web que permita modelar el comportamiento de fluidos mediante cálculos implementados en Python y persistencia de datos mediante Django y PostgreSQL.

## Usuarios

### Profesor

- Administrar usuarios.
- Revisar simulaciones.
- Consultar resultados.
- Exportar información.
- Gestionar actividades académicas.

### Alumno

- Iniciar sesión.
- Crear simulaciones.
- Consultar simulaciones anteriores.
- Comparar resultados.
- Exportar resultados.

## Alcance inicial

La versión inicial incluirá simulaciones de flujo interno en tuberías circulares.

El sistema considerará:

- Diámetro interno.
- Longitud de tubería.
- Rugosidad.
- Velocidad.
- Caudal.
- Densidad.
- Viscosidad.
- Número de Reynolds.
- Régimen de flujo.
- Pérdidas de carga.
- Caída de presión.

## Tecnologías

- Python
- Django
- PostgreSQL
- HTML5
- CSS3
- JavaScript
- Git
- GitHub
- VS Code
- WSL Ubuntu

## Arquitectura

El proyecto usará la arquitectura MVT de Django.

La lógica matemática debe estar separada de la lógica web.

Estructura conceptual:

```text
Formulario web
↓
Vista Django
↓
Motor de cálculo
↓
ORM de Django
↓
PostgreSQL
↓
Resultado almacenado