# Arquitectura de FluidLab

## 1. Visión general

FluidLab es una plataforma web educativa desarrollada en Python y Django para apoyar la enseñanza de Mecánica de Fluidos mediante simulaciones hidráulicas.

La primera versión se enfocará en flujo en tuberías circulares, permitiendo ingresar variables, ejecutar cálculos, guardar resultados y consultar simulaciones anteriores.

## 2. Arquitectura general

El sistema usará la arquitectura MVT de Django:

```text
Usuario
↓
Template
↓
View
↓
Service
↓
Calculations
↓
Model / ORM
↓
PostgreSQL
```

## 3. Aplicaciones Django

### config

Contiene la configuración principal del proyecto Django.

### simulations

Contiene la lógica funcional inicial:

- modelos de simulación;
- formularios;
- vistas;
- servicios;
- cálculos hidráulicos;
- templates;
- tests.

En futuras versiones se podrán separar módulos como:

- accounts;
- pipeflow;
- reports;
- dashboard.

## 4. Separación de responsabilidades

| Archivo | Responsabilidad |
|---|---|
| models.py | Define la estructura de datos persistente |
| forms.py | Valida entradas del usuario |
| views.py | Coordina solicitudes HTTP y respuestas HTML |
| services.py | Coordina la lógica de aplicación |
| calculations.py | Contiene fórmulas hidráulicas |
| templates/ | Contiene la presentación visual |
| tests.py | Contiene pruebas unitarias y funcionales |

## 5. Flujo funcional principal

```text
Alumno inicia sesión
↓
Crea una simulación
↓
Ingresa variables hidráulicas
↓
El formulario valida los datos
↓
El servicio ejecuta los cálculos
↓
Los resultados se guardan
↓
El usuario visualiza el resultado
↓
La simulación queda disponible en el historial
```

## 6. Modelo principal

El modelo central será `Simulation`.

Debe almacenar:

### Datos de usuario

- usuario creador;
- nombre de la simulación;
- descripción.

### Datos de entrada

- diámetro interno;
- longitud de tubería;
- rugosidad;
- velocidad;
- caudal;
- densidad;
- viscosidad dinámica.

### Datos calculados

- área hidráulica;
- número de Reynolds;
- régimen de flujo;
- factor de fricción;
- pérdida de carga;
- caída de presión.

### Metadatos

- fecha de creación;
- fecha de actualización.

## 7. Autenticación y roles

La versión inicial usará el sistema de autenticación nativo de Django.

Roles previstos:

### Profesor

- revisar simulaciones;
- consultar resultados;
- exportar información;
- administrar usuarios desde el panel admin.

### Alumno

- crear simulaciones;
- ver su historial;
- editar sus simulaciones;
- eliminar sus simulaciones.

Para la versión inicial se usarán grupos de Django:

- Profesor
- Alumno

## 8. Base de datos

La base de datos oficial de FluidLab será PostgreSQL.

La aplicación interactuará con la base de datos exclusivamente mediante el ORM de Django.

SQLite no forma parte de la arquitectura prevista del proyecto.

## 9. Motor de cálculo

Las fórmulas hidráulicas deben quedar desacopladas de Django.

El archivo principal será:

```text
simulations/calculations.py
```

Funciones esperadas:

```python
calculate_pipe_area(diameter_m)
calculate_flow_rate(area_m2, velocity_m_s)
calculate_reynolds_number(density, velocity, diameter, dynamic_viscosity)
classify_flow_regime(reynolds_number)
calculate_head_loss(...)
calculate_pressure_drop(...)
```

Las funciones deben:

- usar unidades del Sistema Internacional;
- validar entradas críticas;
- evitar divisiones por cero;
- tener type hints;
- tener docstrings;
- ser testeables sin depender de Django.

## 10. Unidades

| Variable | Unidad |
|---|---|
| Diámetro | m |
| Longitud | m |
| Rugosidad | m |
| Velocidad | m/s |
| Caudal | m³/s |
| Densidad | kg/m³ |
| Viscosidad dinámica | Pa·s |
| Pérdida de carga | m |
| Presión | Pa o kPa |

## 11. Versión 1.0

La versión 1.0 incluirá:

- login/logout;
- CRUD de simulaciones;
- cálculo de área;
- cálculo de caudal;
- número de Reynolds;
- clasificación del régimen de flujo;
- factor de fricción básico;
- pérdida de carga;
- historial por usuario;
- panel admin de Django.

## 12. Fuera de alcance en V1

No se incluirá inicialmente:

- redes de tuberías;
- bombas;
- válvulas;
- canales abiertos;
- dashboard docente avanzado;
- exportación PDF;
- dashboard docente avanzado con métricas, gráficos y seguimiento consolidado;
- simulaciones transitorias;
- modelos CFD.

La versión 1.0 sí permitirá que los profesores consulten las simulaciones asociadas a los cursos que administran. Lo que queda fuera de alcance es un dashboard docente avanzado con indicadores, visualizaciones y analítica académica.

## 13. Principios de diseño

El sistema debe priorizar:

- claridad;
- mantenibilidad;
- separación de responsabilidades;
- trazabilidad de simulaciones;
- facilidad de aprendizaje;
- crecimiento progresivo.

Se debe evitar:

- sobreingeniería;
- dependencias innecesarias;
- lógica matemática en templates;
- lógica matemática extensa en views;
- consultas SQL manuales innecesarias.