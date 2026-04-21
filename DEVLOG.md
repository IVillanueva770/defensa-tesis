# DEVLOG - Defensa de Tesis

## Estado Actual

Repositorio con los materiales de la defensa de tesis de grado de Ignacio Villanueva. Incluye el documento PDF final, scripts de visualización de keypoints, assets de diseño para la presentación, e imágenes para el informe LaTeX.

El subproyecto principal de código es `kp_overlay/`: genera visualizaciones de esqueletos sobre video a partir de JSONs de keypoints COCO WholeBody (133 puntos).

## Tareas Activas

- [ ] (ninguna por ahora)

## Decisiones de Arquitectura

- **Dataset:** Videos de ejercicios físicos con anotaciones COCO WholeBody 133 keypoints/persona.
- **Visualización:** OpenCV para render de esqueletos sobre video; GIFs para assets de presentación.
- **Estructura:** Los videos originales (dataset) se excluyen del repo por tamaño (3.6 GB). Los JSONs de keypoints sí se incluyen como fuente de verdad procesable.

## Sesiones

### 2026-04-21 - Sesión 1
**Objetivo:** Inicializar repositorio git y subir a GitHub

**Hecho:**
- Creado `.gitignore` excluyendo videos originales (3.6 GB), outputs MP4 generados, y video personal
- Inicializado repo git y subido a GitHub
- DEVLOG raíz creado para documentar el proyecto completo

**Próximos pasos:**
- Preparar presentación final
