# Diseño de Base de Datos

## Objetivo

Este documento define el diseño lógico de la base de datos de FluidLab.

La implementación utilizará PostgreSQL mediante el ORM de Django.

No constituye un script SQL, sino la especificación funcional de persistencia.

---

# Motor

PostgreSQL

Acceso mediante Django ORM.

---

# Convenciones

## Claves primarias

Todas las tablas utilizarán una clave primaria autogenerada.

```
id
```

---

## Fechas

Todas las tablas deberán incluir cuando corresponda:

```
created_at
updated_at
```

---

## Estados

Cuando una entidad tenga estado deberá utilizar un campo enumerado.

---

# Tablas

## User

Se utilizará el modelo nativo de Django.

No se creará una tabla personalizada en la versión 1.

---

## Profile

Extiende al usuario.

Campos

- id
- user
- role
- institution
- created_at
- updated_at

Relación

```
User 1 —— 1 Profile
```

---

## Course

Campos

- id
- name
- code
- description
- professor
- academic_year
- semester
- active
- created_at
- updated_at

Relación

```
Professor 1 —— N Courses
```

---

## Enrollment

Tabla intermedia.

Campos

- id
- course
- student
- enrollment_date
- status

Restricción

```
(course, student) UNIQUE
```

---

## Fluid

Campos

- id
- name
- density
- dynamic_viscosity
- reference_temperature
- description
- active
- created_at
- updated_at

---

## CalculationModel

Campos

- id
- name
- version
- description
- active

Ejemplos

Darcy-Weisbach

Colebrook-White

Hazen-Williams

---

## Simulation

Campos generales

- id
- owner
- course
- fluid
- calculation_model
- title
- description
- status

Datos de entrada

- diameter
- length
- roughness
- velocity
- flow_rate
- density_used
- viscosity_used
- gravity

Resultados

- area
- reynolds
- flow_regime
- relative_roughness
- friction_factor
- head_loss
- pressure_drop

Metadatos

- calculation_version
- executed_at
- created_at
- updated_at

---

# Relaciones

```
User

│

├──────1 Profile

│

├──────N Simulation

│

└──────N Enrollment

Course

├──────N Enrollment

└──────N Simulation

Fluid

└──────N Simulation

CalculationModel

└──────N Simulation
```

---

# Restricciones

## Simulation

Debe pertenecer a un usuario.

Debe tener un fluido.

Debe tener un modelo de cálculo.

Debe registrar fecha de ejecución.

---

# Índices recomendados

Simulation

- owner
- created_at
- course
- status

Course

- code

Fluid

- name

CalculationModel

- name

---

# Estrategia ORM

Se utilizarán:

ForeignKey

OneToOneField

Choices

TextChoices

Model Managers cuando sea necesario.

No utilizar SQL manual.

---

# Eliminación

Profile

Eliminar junto con el usuario.

Simulation

No eliminar automáticamente al eliminar un curso.

Enrollment

Eliminar al eliminar curso o alumno.

Fluid

No eliminar si existen simulaciones asociadas.

CalculationModel

No eliminar si existen simulaciones asociadas.

---

# Versionamiento

El esquema será administrado mediante migraciones de Django.

No modificar migraciones ya aplicadas.

Toda modificación deberá generar una nueva migración.

---

# Objetivo

La base de datos debe privilegiar:

- simplicidad;
- integridad;
- trazabilidad;
- escalabilidad;
- compatibilidad con PostgreSQL.