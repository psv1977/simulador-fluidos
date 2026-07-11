# FluidLab

> Plataforma web educativa para la simulación de Mecánica de Fluidos desarrollada con Python y Django.

---

## Descripción

FluidLab es una aplicación web diseñada para apoyar la enseñanza y el aprendizaje de Mecánica de Fluidos mediante simulaciones numéricas ejecutadas desde un navegador.

La primera versión está orientada al estudio del flujo interno en tuberías circulares, permitiendo a profesores y estudiantes crear, almacenar y analizar simulaciones utilizando modelos matemáticos implementados en Python.

Los resultados son almacenados en PostgreSQL utilizando el ORM de Django, permitiendo mantener un historial completo de las simulaciones realizadas.

---

# Objetivos

- Facilitar el aprendizaje de Mecánica de Fluidos.
- Permitir la ejecución de simulaciones hidráulicas desde un navegador.
- Almacenar todas las simulaciones realizadas por los usuarios.
- Implementar modelos matemáticos utilizando Python.
- Utilizar buenas prácticas de desarrollo con Django.

---

# Características principales

- Autenticación de usuarios.
- Gestión de profesores y alumnos.
- Simulación de flujo en tuberías.
- Almacenamiento histórico de simulaciones.
- Base de datos PostgreSQL.
- Arquitectura MVT de Django.
- Motor de cálculo desacoplado de la interfaz.

---

# Tecnologías

| Tecnología | Uso |
|------------|-----|
| Python | Lenguaje principal |
| Django | Framework Web |
| PostgreSQL | Base de datos |
| HTML5 | Interfaz |
| CSS3 | Estilos |
| JavaScript | Interactividad |
| Git | Control de versiones |
| GitHub | Repositorio |
| VS Code | IDE |
| WSL Ubuntu | Entorno de desarrollo |

---

# Arquitectura

La arquitectura completa del proyecto se encuentra documentada en:

```
docs/ARCHITECTURE.md
```

El modelo de dominio se encuentra en:

```
docs/DOMAIN_MODEL.md
```

---

# Estructura del proyecto

```text
fluid_lab/

├── config/
├── simulations/
├── docs/
│   ├── ARCHITECTURE.md
│   └── DOMAIN_MODEL.md
├── AGENTS.md
├── PROJECT.md
├── README.md
├── requirements.txt
├── manage.py
└── LICENSE
```

---

# Instalación

Clonar el repositorio:

```bash
git clone https://github.com/TU_USUARIO/fluid_lab.git
```

Entrar al proyecto:

```bash
cd fluid_lab
```

Crear entorno virtual:

```bash
python3 -m venv venv
```

Activar entorno virtual:

Linux / WSL

```bash
source venv/bin/activate
```

Windows

```powershell
venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar migraciones:

```bash
python manage.py migrate
```

Iniciar servidor:

```bash
python manage.py runserver
```

---

# Estado del proyecto

Actualmente se encuentra en desarrollo.

Versión prevista:

```
FluidLab 1.0
```

---

# Roadmap

## V1

- Login
- CRUD de simulaciones
- Reynolds
- Darcy-Weisbach
- Historial

## V2

- Colebrook-White
- Moody
- Dashboard docente
- Exportación Excel

## V3

- Bombas
- Válvulas
- Redes de tuberías
- Canales abiertos

---

# Licencia

Este proyecto está distribuido bajo la licencia MIT.

Ver archivo:

```
LICENSE
```

---

# Autor

**Patricio Saavedra**

Ingeniero Mecánico

Proyecto desarrollado utilizando Python, Django y PostgreSQL.