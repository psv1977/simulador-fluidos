# Changelog

Todos los cambios relevantes de FluidaLab se documentarán en este archivo.

El formato sigue una estructura simple basada en versiones y categorías de cambios.

---

## [1.1.0] - 2026-07-28

### Agregado

- Slider interactivo para modificar el diámetro interno de la tubería.
- Cálculo instantáneo del área transversal.
- Cálculo instantáneo de la velocidad media.
- Cálculo instantáneo del número de Reynolds.
- Clasificación automática del régimen de flujo.
- Visualización longitudinal de la tubería.
- Representación cualitativa del perfil de velocidades.
- Diferenciación visual entre flujo laminar, transicional y turbulento.
- Botón para guardar simulaciones en la base de datos.
- Actualización del README en español e inglés.

### Modificado

- El botón `Calcular` fue reemplazado por `Guardar simulación`.
- El formulario dejó de depender de una recarga para mostrar resultados.
- Se reorganizó la interfaz del simulador.
- Se separó la lógica interactiva en un archivo JavaScript independiente.
- Se actualizaron los estilos del simulador para la versión 1.1.

---

## [1.0.0] - 2026-07-13

### Agregado

- Motor de cálculo hidráulico inicial.
- Cálculo de área transversal.
- Cálculo de velocidad media.
- Cálculo del número de Reynolds.
- Clasificación del régimen de flujo.
- Registro e inicio de sesión de usuarios.
- Almacenamiento de simulaciones.
- Historial personal de simulaciones.
- Integración con Django Admin.
- Pruebas unitarias y pruebas de integración con Django.