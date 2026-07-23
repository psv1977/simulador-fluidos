# 🌊 FluidaLab

> **FluidaLab** es una aplicación web desarrollada con **Python** y **Django** para realizar simulaciones hidráulicas en tuberías, almacenar los resultados obtenidos y administrar el historial de simulaciones de cada usuario mediante una arquitectura web moderna basada en el patrón **MVT (Model–View–Template)**.

---

# Descripción

FluidaLab nace como una plataforma para el desarrollo de herramientas de ingeniería hidráulica accesibles desde un navegador web.

La versión **1.0.0** implementa un simulador hidráulico básico que permite calcular parámetros fundamentales del flujo en tuberías circulares, almacenar cada simulación realizada y consultar posteriormente su historial.

Aunque esta primera versión se centra en un único modelo hidráulico, la arquitectura fue diseñada desde el inicio para permitir la incorporación de nuevos modelos de cálculo y futuras funcionalidades sin modificar la estructura principal del sistema.

---

# Objetivos del proyecto

Los principales objetivos de FluidaLab son:

- Desarrollar una aplicación web utilizando Django.
- Implementar una arquitectura escalable basada en MVT.
- Separar la lógica hidráulica de la interfaz gráfica.
- Almacenar todas las simulaciones realizadas por cada usuario.
- Servir como base para futuras herramientas de simulación hidráulica.

---

# Funcionalidades de la versión 1.0

## Gestión de usuarios

- Inicio de sesión.
- Cierre de sesión.
- Protección mediante autenticación.
- Cada usuario accede únicamente a sus propias simulaciones.

---

## Simulación hidráulica

El sistema calcula automáticamente:

- Área transversal de la tubería.
- Velocidad media del flujo.
- Número de Reynolds.
- Clasificación automática del régimen de flujo:
  - Laminar
  - Transicional
  - Turbulento

---

## Persistencia

Cada simulación queda almacenada en la base de datos incluyendo:

- Usuario propietario.
- Fecha de creación.
- Parámetros de entrada.
- Resultados calculados.
- Estado de la simulación.
- Modelo de cálculo utilizado.
- Versión del algoritmo de cálculo.

---

## Historial de simulaciones

Cada usuario puede:

- visualizar todas sus simulaciones;
- consultar el detalle completo de cada una;
- crear nuevas simulaciones;
- acceder únicamente a sus propios registros.

---

# Tecnologías utilizadas

| Tecnología | Uso |
|------------|-----|
| Python 3.14 | Lenguaje principal |
| Django 6 | Framework web |
| SQLite | Base de datos de desarrollo |
| HTML5 | Plantillas |
| CSS3 | Interfaz gráfica |
| Git | Control de versiones |
| GitHub | Repositorio |

---

# Arquitectura del sistema

FluidaLab sigue el patrón arquitectónico **MVT (Model–View–Template)** implementado por Django.

```
                  Usuario
                      │
                      ▼
                  URL Dispatcher
                      │
                      ▼
                  Views.py
                 (Lógica)
                ╱          ╲
               ▼            ▼
         Models.py      Templates
              │             │
              └──────┬──────┘
                     ▼
                Base de datos
```

## Componentes

### Models

Representan las entidades del sistema y administran el acceso a la base de datos mediante el ORM de Django.

### Views

Procesan las solicitudes HTTP, ejecutan la lógica del simulador hidráulico y generan el contexto enviado a las plantillas.

### Templates

Construyen la interfaz gráfica utilizando HTML y el motor de plantillas de Django.

---

# Estructura del proyecto

```
simulador-fluidos/

│
├── config/
│
├── simulations/
│   ├── calculations.py
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   ├── migrations/
│   ├── static/
│   └── templates/
│
├── manage.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

# Uso de la aplicación

FluidaLab fue concebida como una aplicación web.

Una vez desplegada en un servidor, los usuarios únicamente deberán acceder mediante un navegador web e iniciar sesión con sus credenciales.

No será necesario instalar Python ni descargar el proyecto para utilizar la aplicación.

---

# Instalación para desarrollo

Las siguientes instrucciones están dirigidas únicamente a desarrolladores que deseen ejecutar el proyecto localmente.

## Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/simulador-fluidos.git
```

Entrar al proyecto

```bash
cd simulador-fluidos
```

Crear entorno virtual

```bash
python -m venv venv
```

Activarlo

Linux / WSL

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

Aplicar migraciones

```bash
python manage.py migrate
```

Crear superusuario

```bash
python manage.py createsuperuser
```

Ejecutar el servidor

```bash
python manage.py runserver
```

Abrir:

```
http://127.0.0.1:8000/simulations/
```

---

# Pruebas automatizadas

El proyecto incorpora pruebas automatizadas para validar tanto el motor hidráulico como el funcionamiento de la aplicación web.

Ejecutar:

```bash
python manage.py test simulations
```

Estado actual:

- 25 pruebas automatizadas.
- Todas aprobadas.

---

# Modelo de datos

Las principales entidades del sistema son:

- User
- Profile
- Course
- Enrollment
- Fluid
- CalculationModel
- Simulation

La entidad principal corresponde a **Simulation**, donde se almacenan tanto los parámetros de entrada como los resultados obtenidos en cada cálculo.

---

# Seguridad

FluidaLab incorpora:

- autenticación mediante Django Authentication;
- protección CSRF;
- acceso restringido a usuarios autenticados;
- aislamiento de las simulaciones por usuario.

---

# Capturas de pantalla

Se recomienda incorporar las siguientes imágenes:

- Pantalla de inicio de sesión.
- Nueva simulación.
- Historial de simulaciones.
- Detalle de simulación.
- Panel de administración de Django.

---

# Roadmap

## Versión 1.0.0

- ✔ Motor hidráulico.
- ✔ Arquitectura MVT.
- ✔ Persistencia mediante ORM.
- ✔ Autenticación.
- ✔ Historial de simulaciones.
- ✔ Detalle de simulaciones.
- ✔ Interfaz web.
- ✔ Pruebas automatizadas.

---

## Versión 1.1

- Exportación CSV.
- Eliminación de simulaciones.
- Filtros de búsqueda.
- Mejoras de interfaz.

---

## Versión 2.0

- Cálculo de pérdidas de carga.
- Darcy–Weisbach.
- Colebrook–White.
- Diagrama de Moody.
- Comparación entre simulaciones.
- Múltiples modelos hidráulicos.
- API REST.
- Exportación PDF.
- Gráficos interactivos.

---

# Autor

**Patricio Saavedra**

Ingeniero Mecánico.

Especialista en mantenimiento predictivo, confiabilidad industrial y desarrollo de aplicaciones técnicas utilizando Python y Django.

---

# Licencia

Este proyecto se distribuye bajo la licencia MIT.

---

# Estado del proyecto

**Versión actual: v1.0.0**

FluidaLab se encuentra en una versión funcional y estable que implementa la arquitectura base del sistema, el primer modelo hidráulico y la infraestructura necesaria para continuar su evolución hacia una plataforma de simulación hidráulica de mayor alcance.