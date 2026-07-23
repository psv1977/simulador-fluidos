# Modelo de dominio de FluidLab

## 1. Propósito

Este documento define las entidades principales, sus responsabilidades y sus relaciones dentro de FluidLab.

FluidLab es una plataforma web educativa para ejecutar, almacenar y analizar simulaciones relacionadas con Mecánica de Fluidos.

La versión 1.0 estará enfocada en el flujo estacionario de fluidos en tuberías circulares.

---

## 2. Alcance del modelo de dominio

El modelo inicial debe permitir:

- autenticar profesores y alumnos;
- identificar el rol de cada usuario;
- registrar simulaciones realizadas por los alumnos;
- almacenar los datos de entrada;
- almacenar los resultados calculados;
- consultar el historial de simulaciones;
- permitir que los profesores revisen el trabajo de los alumnos;
- mantener trazabilidad de la fecha y autor de cada simulación.

La versión inicial no modelará todavía:

- redes completas de tuberías;
- múltiples tramos dentro de una misma simulación;
- bombas;
- válvulas;
- canales abiertos;
- flujo transitorio;
- modelos CFD.

---

## 3. Entidades principales

Las entidades principales de FluidLab 1.0 serán:

1. Usuario
2. Perfil de usuario
3. Curso
4. Inscripción en curso
5. Simulación
6. Fluido

---

## 4. Diagrama conceptual

```text
Usuario
   │
   │ 1
   │
   │ 1
   ▼
Perfil de usuario

Profesor
   │
   │ crea o administra
   ▼
Curso
   │
   │ 1
   │
   │ N
   ▼
Inscripción
   ▲
   │ N
   │
   │ 1
Alumno

Usuario
   │
   │ 1
   │
   │ N
   ▼
Simulación
   │
   │ N
   │
   │ 1
   ▼
Fluido

Curso
   │
   │ 1
   │
   │ N
   ▼
Simulación
```

---

## 5. Usuario

### Descripción

Representa a una persona autenticada dentro de FluidLab.

Para esta entidad se utilizará inicialmente el modelo de usuario incluido en Django.

No se creará un modelo de autenticación personalizado durante la primera versión, salvo que aparezca un requerimiento que lo justifique.

### Datos principales

- nombre de usuario;
- nombre;
- apellido;
- correo electrónico;
- contraseña cifrada;
- estado activo;
- fecha de registro;
- último acceso.

### Responsabilidades

Un usuario puede:

- iniciar y cerrar sesión;
- actualizar sus datos básicos;
- acceder a funcionalidades según su rol;
- ser propietario de simulaciones;
- pertenecer a uno o más cursos.

### Implementación prevista

Se utilizará:

```python
django.contrib.auth.models.User
```

Los permisos podrán administrarse mediante:

- grupos de Django;
- permisos de Django;
- validaciones de autorización en las vistas.

---

## 6. Perfil de usuario

### Descripción

Complementa al usuario de Django con información específica de FluidLab.

### Datos propuestos

- usuario;
- rol principal;
- identificador académico opcional;
- institución opcional;
- fecha de creación;
- fecha de actualización.

### Roles iniciales

- Profesor
- Alumno

### Relación

```text
Usuario 1 ─── 1 Perfil de usuario
```

Cada usuario tendrá como máximo un perfil.

### Observación de diseño

Los grupos de Django podrán utilizarse para permisos generales. El perfil permitirá guardar información académica adicional.

---

## 7. Curso

### Descripción

Representa una asignatura, sección o grupo académico administrado por un profesor.

### Datos propuestos

- nombre;
- código;
- descripción;
- profesor responsable;
- año académico;
- período académico;
- estado activo;
- fecha de creación;
- fecha de actualización.

### Ejemplos

```text
Mecánica de Fluidos I
MFL-201
Primer semestre 2026
```

### Relaciones

```text
Profesor 1 ─── N Cursos
Curso N ─── N Alumnos
Curso 1 ─── N Simulaciones
```

### Responsabilidades

Un curso permite:

- agrupar alumnos;
- asociar simulaciones a una asignatura;
- facilitar la revisión docente;
- filtrar el historial por período académico.

---

## 8. Inscripción en curso

### Descripción

Representa la participación de un alumno en un curso.

Esta entidad resuelve la relación de muchos a muchos entre alumnos y cursos.

### Datos propuestos

- curso;
- alumno;
- fecha de inscripción;
- estado;
- fecha de creación.

### Estados posibles

- activa;
- finalizada;
- retirada.

### Relación

```text
Alumno 1 ─── N Inscripciones
Curso 1 ─── N Inscripciones
```

### Restricción

Un alumno no debe inscribirse más de una vez en el mismo curso.

La combinación de curso y alumno debe ser única.

---

## 9. Fluido

### Descripción

Representa las propiedades físicas de un fluido utilizado en una simulación.

Esta entidad evita repetir manualmente las propiedades de fluidos conocidos y permite agregar nuevos fluidos en el futuro.

### Datos propuestos

- nombre;
- densidad;
- viscosidad dinámica;
- temperatura de referencia;
- descripción;
- estado activo;
- fecha de creación;
- fecha de actualización.

### Unidades

| Propiedad | Unidad SI |
|---|---|
| Densidad | kg/m³ |
| Viscosidad dinámica | Pa·s |
| Temperatura | °C |

### Ejemplos

- agua a 20 °C;
- aire a 20 °C;
- aceite hidráulico;
- fluido personalizado.

### Relación

```text
Fluido 1 ─── N Simulaciones
```

### Consideración técnica

Las propiedades de un fluido dependen de la temperatura. En FluidLab 1.0 se almacenarán valores correspondientes a una temperatura de referencia.

Una versión posterior podrá incorporar propiedades variables con la temperatura.

---

## 10. Simulación

### Descripción

Es la entidad central de FluidLab.

Representa un caso de análisis ejecutado por un usuario y contiene tanto los datos ingresados como los resultados calculados.

### Identificación

- identificador interno;
- nombre;
- descripción;
- usuario propietario;
- curso asociado opcional;
- fluido utilizado;
- estado de la simulación.

### Datos de entrada

- diámetro interno de la tubería;
- longitud de la tubería;
- rugosidad absoluta;
- velocidad media;
- caudal volumétrico;
- densidad del fluido;
- viscosidad dinámica;
- aceleración de gravedad.

### Resultados calculados

- área transversal;
- velocidad calculada;
- caudal calculado;
- número de Reynolds;
- régimen de flujo;
- rugosidad relativa;
- factor de fricción;
- pérdida de carga;
- caída de presión.

### Metadatos

- fecha y hora de creación;
- fecha y hora de actualización;
- fecha y hora de ejecución;
- versión del modelo de cálculo.

### Relaciones

```text
Usuario 1 ─── N Simulaciones
Curso 1 ─── N Simulaciones
Fluido 1 ─── N Simulaciones
```

La relación con Curso podrá ser opcional para permitir simulaciones libres fuera de una actividad académica.

---

## 11. Estados de una simulación

Una simulación podrá tener los siguientes estados:

- borrador;
- calculada;
- inválida;
- archivada.

### Borrador

La simulación fue creada, pero todavía no se han ejecutado correctamente los cálculos.

### Calculada

Los datos fueron validados y los resultados fueron generados correctamente.

### Inválida

Los datos no permiten ejecutar el modelo de cálculo.

### Archivada

La simulación se conserva como historial, pero ya no está activa para edición ordinaria.

---

## 12. Régimen de flujo

El régimen de flujo se determinará a partir del número de Reynolds.

Los valores iniciales serán:

- laminar;
- transicional;
- turbulento.

El régimen será un resultado calculado, no una entrada proporcionada por el usuario.

Los límites utilizados deberán estar documentados en el motor de cálculo y cubiertos por pruebas unitarias.

---

## 13. Reglas de negocio

### RN-01: autenticación

Solo los usuarios autenticados pueden crear y consultar simulaciones.

### RN-02: propiedad

Cada simulación debe pertenecer a un usuario.

### RN-03: acceso del alumno

Un alumno puede consultar y modificar solamente sus propias simulaciones, salvo permisos expresamente definidos.

### RN-04: acceso del profesor

Un profesor puede consultar las simulaciones asociadas a los cursos que administra.

### RN-05: asociación con curso

Una simulación puede estar asociada a un curso, pero esta relación será opcional para permitir simulaciones libres.

### RN-06: datos positivos

Los siguientes valores deben ser mayores que cero:

- diámetro;
- longitud;
- densidad;
- viscosidad dinámica;
- aceleración de gravedad.

### RN-07: velocidad o caudal

La simulación debe recibir al menos uno de estos valores:

- velocidad;
- caudal.

Si se proporciona solo uno, el otro debe calcularse mediante el área de la tubería.

### RN-08: coherencia hidráulica

Si se proporcionan simultáneamente velocidad y caudal, el sistema debe verificar su coherencia con el diámetro ingresado.

### RN-09: almacenamiento de resultados

Los resultados solamente deben guardarse cuando las entradas hayan sido validadas correctamente.

### RN-10: unidades internas

Todos los cálculos y datos persistidos deben usar unidades del Sistema Internacional.

### RN-11: trazabilidad

Cada simulación debe registrar:

- usuario responsable;
- fecha de creación;
- fecha de modificación;
- fecha de ejecución;
- versión del motor de cálculo.

### RN-12: eliminación

Las simulaciones no deben eliminarse automáticamente al eliminar un curso.

El comportamiento exacto debe definirse mediante una política de eliminación segura.

### RN-13: reproducción

Una simulación guardada debe contener suficiente información para reproducir sus resultados posteriormente.

---

## 14. Datos del fluido dentro de la simulación

Aunque una simulación esté relacionada con un registro de Fluido, también debe guardar una copia de las propiedades físicas utilizadas durante el cálculo:

- densidad utilizada;
- viscosidad utilizada;
- temperatura de referencia utilizada.

Esto permite conservar la trazabilidad si posteriormente se modifican las propiedades del fluido almacenado en el catálogo.

Ejemplo:

```text
El catálogo de Agua cambia su densidad de referencia.
Una simulación anterior debe conservar el valor con el cual fue calculada.
```

---

## 15. Separación entre datos de entrada y resultados

En FluidLab 1.0 los datos de entrada y resultados podrán almacenarse en una misma entidad `Simulation`.

Esta decisión simplifica:

- el CRUD;
- los formularios;
- el historial;
- las consultas ORM;
- la administración desde Django Admin.

En FluidLab 1.0 no existirá un modelo independiente denominado `SimulationResult`.

Los datos de entrada y los resultados calculados se almacenarán en la entidad `Simulation`.

Una separación entre `Simulation` y `SimulationResult` podrá evaluarse en versiones futuras cuando una misma simulación requiera múltiples ejecuciones o escenarios.

Una separación posterior puede justificarse si:

- una simulación genera múltiples ejecuciones;
- se necesita comparar diferentes iteraciones;
- se implementa versionado completo de resultados;
- los resultados aumentan considerablemente.

---

## 16. Modelo conceptual inicial para Django

La implementación inicial podrá basarse en los siguientes modelos:

```text
User
Profile
Course
Enrollment
Fluid
Simulation
CalculationModel
```

Relaciones:

```text
User 1 ─── 1 Profile

User (profesor) 1 ─── N Course

User (alumno) 1 ─── N Enrollment
Course 1 ─── N Enrollment

User 1 ─── N Simulation
Course 1 ─── N Simulation
Fluid 1 ─── N Simulation
```

---

## 17. Decisiones de diseño para la versión 1.0

### Se utilizará el usuario estándar de Django

No se implementará todavía un modelo de usuario personalizado.

### Los roles usarán grupos y perfiles

Los grupos controlarán permisos generales y el perfil almacenará información académica adicional.

### Una simulación tendrá una tubería

Cada simulación de la versión inicial representará una sola tubería circular.

### Entrada y resultado compartirán un modelo

Se priorizará una implementación simple y mantenible.

### Los cálculos estarán fuera de los modelos

Las fórmulas hidráulicas se implementarán en funciones de Python independientes.

### PostgreSQL se utilizará mediante el ORM

No se utilizará SQL crudo salvo necesidad técnica documentada.

---

## 18. Evolución futura

El modelo debe poder evolucionar posteriormente hacia:

- actividades o ejercicios creados por profesores;
- entregas de alumnos;
- varias ejecuciones por simulación;
- comparación de escenarios;
- tuberías en serie y paralelo;
- redes hidráulicas;
- accesorios y pérdidas menores;
- bombas;
- válvulas;
- canales abiertos;
- reportes académicos;
- exportación de resultados;
- panel de seguimiento docente.

Cuando una simulación necesite contener varios componentes hidráulicos, podrá incorporarse una entidad como:

```text
Simulation
   │
   └── N HydraulicComponents
           ├── Pipe
           ├── Pump
           ├── Valve
           └── Fitting
```

Esta estructura no se implementará en FluidLab 1.0.

---

## 19. Resumen

El núcleo funcional de FluidLab 1.0 será la entidad `Simulation`.

Cada simulación:

- pertenece a un usuario;
- puede asociarse a un curso;
- utiliza un fluido;
- contiene variables de entrada;
- almacena resultados calculados;
- mantiene trazabilidad;
- puede consultarse en el historial.

El modelo inicial prioriza simplicidad, claridad académica y crecimiento progresivo.