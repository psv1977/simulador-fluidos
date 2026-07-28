🌊 FluidaLab

Plataforma abierta para simulación hidráulica interactiva,visualización de fenómenos de Mecánica de Fluidos y apoyo a laenseñanza de la ingeniería.Open platform for interactive hydraulic simulation, Fluid Mechanicsvisualization and engineering education.



🇪🇸 Español

Descripción

FluidaLab es una plataforma web desarrollada con Python yDjango para el análisis, simulación y visualización interactiva delflujo interno en tuberías.

Más que una calculadora hidráulica, FluidaLab busca transformarse en unaplataforma modular donde estudiantes, docentes e ingenieros puedancomprender los fenómenos de Mecánica de Fluidos mediante simulacionesdinámicas, representaciones visuales y modelos de cálculo basados enprincipios físicos.

La arquitectura fue diseñada desde el inicio para permitir incorporarnuevos modelos hidráulicos sin modificar la estructura principal delsistema.

Objetivos

Facilitar la comprensión de la Mecánica de Fluidos mediantesimulaciones interactivas.

Desarrollar una plataforma modular para herramientas hidráulicas.

Separar completamente el motor de cálculo de la interfaz gráfica.

Almacenar el historial de simulaciones de cada usuario.

Permitir la incorporación de nuevos modelos de cálculo yvisualización.

Características de la versión 1.1

Gestión de usuarios

Registro e inicio de sesión.

Protección mediante autenticación de Django.

Historial individual de simulaciones.

Simulación interactiva

Slider para modificar el diámetro interno.

Actualización instantánea de:

Área transversal.

Velocidad media.

Número de Reynolds.

Régimen del flujo.

Visualización longitudinal de la tubería.

Representación cualitativa del perfil de velocidades.

Persistencia de simulaciones.

Tecnologías

Tecnología     Uso

Python         Lenguaje principalDjango 6       Framework webHTML5          PlantillasCSS3           EstilosJavaScript     Interactividad en tiempo realSQLite         DesarrolloPostgreSQL     Producción (planificado)Git / GitHub   Control de versiones

Arquitectura

FluidaLab sigue el patrón MVT (Model--View--Template).

Usuario
   │
   ▼
URL Dispatcher
   │
   ▼
Views
╱      ╲
▼       ▼
Models Templates
   │
   ▼
Base de datos

La lógica hidráulica permanece desacoplada de la interfaz gráfica,permitiendo reutilizar el motor de cálculo y extender el proyecto connuevos módulos.

Modelo hidráulico actual

El sistema calcula automáticamente:

Área transversal

Velocidad media

Número de Reynolds

Régimen de flujo (Laminar, Transicional y Turbulento)

Roadmap

✔ Versión 1.1

Simulación interactiva.

Slider de diámetro.

Perfil longitudinal.

Perfil de velocidades.

Persistencia de simulaciones.

🚧 Versión 1.2

Biblioteca de fluidos.

Biblioteca de materiales.

Selección automática de propiedades.

Mejoras de visualización.

🔬 Versión 1.5

Darcy--Weisbach.

Colebrook--White.

Diagrama de Moody.

🚀 Versión 2.0

Redes de tuberías.

Bombas.

Accesorios.

API REST.

Reportes.

Módulos educativos.

Filosofía

El software de ingeniería no debería limitarse a entregar resultadosnuméricos. También debería ayudar a comprender los fenómenos físicosque existen detrás de cada cálculo.

Desarrollo

Instalación

git clone <repositorio>
cd FluidaLab

python -m venv .venv

# Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Pruebas

python manage.py test simulations

Historial de versiones

El detalle de cada versión se documenta en CHANGELOG.md.

🇬🇧 English

Overview

FluidaLab is an open web platform for hydraulic simulation, interactivevisualization and Fluid Mechanics education developed with Python andDjango.

The project combines engineering calculations, real-time visualizationand simulation management within a modular architecture designed toevolve into a complete hydraulic engineering platform.

Current features

Interactive hydraulic simulation.

Real-time Reynolds calculation.

Longitudinal pipe visualization.

Qualitative velocity profile.

User authentication.

Simulation persistence.

Modular Django architecture.

Development Philosophy

Engineering software should not only produce accurate numericalresults. It should also help engineers understand the physicalphenomena behind those results.

Author

Patricio Saavedra

Mechanical Engineer | MBA

Engineering Consultant • Software Developer

License

MIT License