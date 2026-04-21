# DEVLOG - kp_overlay

## Estado Actual

Script `render_skeletons.py` funcional. Lee los 6 JSONs de keypoints (COCO WholeBody, 133 puntos/persona) y genera un MP4 por archivo con esqueletos sobre fondo negro. Modo por defecto: `body+hands`, threshold de confianza 0.3, 25 FPS.

## Tareas Activas

- [ ] (ninguna por ahora)

## Decisiones de Arquitectura

- **Formato keypoints**: COCO WholeBody 133 puntos (0-16 body, 17-22 feet, 23-90 face-68, 91-111 left hand, 112-132 right hand)
- **Canvas dinámico**: se calcula el bounding box de todos los puntos con score >= threshold a lo largo del video, con 10% de padding. El lado mayor se escala a 720px.
- **Colores por ID de persona**: se asignan antes de iterar los frames para que el mismo ID mantenga color constante aunque aparezca/desaparezca.
- **Threshold 0.3**: balance entre ruido y completitud. Configurable en la constante `CONF_THRESHOLD`.
- **Fallback de codec**: si `mp4v` falla en Windows, usa `XVID` con `.avi`.

## Sesiones

### 2026-04-20 - Sesión 1
**Objetivo:** Generar videos de esqueletos a partir de los JSONs de keypoints

**Hecho:**
- Exploración de la estructura de los JSONs (confirmado: COCO WholeBody 133kp, frames como lista de dicts)
- Creación de `render_skeletons.py` con pipeline completo
- Generación exitosa de 6 MP4 en `output/`

**Decisiones:**
- Usar OpenCV para VideoWriter (sin ffmpeg ni matplotlib para el render principal)
- Filtrar por confidence >= 0.3 antes de dibujar cualquier punto o conexión
- Modo `body+hands` como default (más legible que `full` con cara)

**Próximos pasos:**
- Ajustar threshold si algún video se ve ruidoso o incompleto
- Opcional: agregar número de frame o nombre de persona en el video
