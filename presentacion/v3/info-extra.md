# Info extra — Defensa de tesis

Contexto y material de soporte que no va ni en las slides ni en el guion, pero que conviene tener a mano al producir la presentación y al ensayar.

---

## Principios de diseño aplicados

- Una idea por slide.
- Poco texto; la voz sostiene la narrativa.
- Peso técnico preservado (es defensa de grado, no keynote comercial).
- Estructura en 5 actos con puentes verbales entre ellos.

---

## Sistema de estilos

- **Fondo**: gris muy oscuro casi negro (`#1C1C1C`).
- **Acento primario**: amarillo vibrante (`#F5D547`) — títulos, cifras grandes, pills de sección.
- **Acento secundario**: naranja cálido (`#E67E4A`) — solo para cifras clave y contrastes puntuales.
- **Texto cuerpo**: blanco suave (`#F2F2F2` lead, `#C5C5C5` cuerpo).
- **Tipografía**: serif-bold amarillo para H1 (estilo Recoleta), sans-serif blanco para cuerpo.
- **Pills de sección**: rectángulo con esquinas redondeadas, fondo marrón oscuro, borde amarillo tenue, texto amarillo en mayúsculas.
- **Cards**: fondo gris medio, borde izquierdo amarillo vertical.
- **Tablas**: sin bordes externos, separadores sutiles, filas destacadas con fondo amarillo translúcido.
- **Flechas/iconografía**: línea fina amarilla, iconos minimalistas monocromo.

---

## Estructura narrativa: 5 actos, 23 slides

| Acto | Slides | Pregunta que responde |
|------|--------|----------------------|
| Apertura | S1–S2 | Portada y agenda |
| I — La pregunta | S3–S6 | ¿Qué problema? + ¿qué me comprometí a resolver? |
| II — El sistema | S7–S11 | ¿Cómo lo resolví? |
| III — El recorrido experimental | S12–S15 | ¿Cómo llegué al número? |
| IV — Resultados | S16–S19 | ¿Qué logré? |
| V — Cierre y proyección | S20–S23 | ¿Hacia dónde sigue? |

Entre actos va un **puente verbal** (frase hablada del presentador, no slide) que lleva la atención al siguiente acto.

---

## Cronograma estimado

| Acto | Slides | Duración |
|------|--------|----------|
| Apertura | S1–S2 | 40 seg |
| Acto I | S3–S6 | 3:00 |
| Acto II | S7–S11 | 4:30 |
| Acto III | S12–S15 | 3:40 |
| Acto IV | S16–S19 | 3:00 |
| Acto V | S20–S23 | 3:15 |
| **Total** | 23 slides | **~18–19 min** |

Margen de ~2–3 min para respirar, pausas, y puentes verbales entre actos bien marcados. Total operativo: **~20 min**.

---

## Placeholders de assets por slide

Slides que requieren insertar asset manualmente después de generar en Gamma:

| Slide | Tipo | Descripción |
|-------|------|-------------|
| S3 | GIF | Persona haciendo press de hombro con skeleton de keypoints superpuesto |
| S8 | Figura | Arquitectura Vision Transformer (parches + embedding + encoder) |
| S9 | Figura | Volumen 3D con eje temporal (cubo de heatmaps apilados) |
| S10 | GIF / tira | 5 frames con bounding boxes e IDs cambiando entre frames |
| S13 | Figura | Curva de pérdida experimento base (train vs. val divergentes) |
| S14 | Figura | Curva de pérdida con transfer learning (brecha más chica) |
| S15 | Figura | Curva de precisión configuración final (convergencia estable) |
| S17 | Figura | Matriz de confusión 3×3 con diagonal dominante |
| S19 | GIF | Sistema funcionando — video con skeleton + etiqueta de predicción |

Las figuras de curvas y matriz de confusión están en el paper (Figuras 12, 14, 16, 18).

---

## Verificación antes de la defensa

- Cronometrar el slideshow completo con el guion real. Objetivo: 18–22 min.
- Leer cada slide en voz alta sin notas. Si el texto del slide repite lo que decís, sobra texto.
- Ensayar los 4 puentes verbales entre actos (Acto I→II, II→III, III→IV, IV→V).
- Verificar la reproducción de los GIFs/videos en el equipo del día de la defensa.

---

## Aprobaciones pendientes

Antes de insertar assets finales o cerrar la versión:

1. ¿El guion conserva la voz de Ignacio (tono, jerga técnica, nivel de formalidad) o hay que ajustar el registro?
2. ¿La frase personal de S23 queda bien o preferís una alternativa del capítulo "Reflexión Final" del paper?
3. ¿El orden del guion en los experimentos (S13–S15) refleja bien cómo lo viviste, o hay algún matiz técnico que quieras agregar?
4. Elegir qué GIF específico va en cada uno de los placeholders (S3, S10, S19) — hay varios disponibles en el repo.
