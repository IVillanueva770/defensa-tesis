# Delta v3 — Actualización PPT
## Base: presentación actual de 10 slides (Gamma)

---

## PARTE 1: SLIDES NUEVAS A INSERTAR

### NUEVA — "¿Por qué ViTPose?"
**Posición:** insertar entre slide 5 (La Solución: El Pipeline) y slide 6 (El Problema del Tracking)

Diseño: dos columnas, sin fórmulas, visual-first. Fondo oscuro.

- Columna izquierda — "Otras herramientas (OpenPose, MediaPipe)":
  - Analizan la imagen en partes pequeñas, de forma local
  - Para conectar codo con hombro, necesitan combinar muchas piezas de información por separado
- Columna derecha — "ViTPose":
  - Ve todas las articulaciones en relación al mismo tiempo
  - Entiende de un vistazo cómo el codo se conecta con el hombro y la muñeca
- **Texto destacado:** "ViTPose entiende el cuerpo como un todo, no como una suma de partes."

---

### NUEVA — "La lógica de los experimentos"
**Posición:** insertar entre slide 6 (Tracking) y slide 7 (Evolución del Rendimiento)

Diseño: diagrama de flujo o 3 columnas encadenadas con flechas. Fondo oscuro. Texto conciso — los números detallados están en el slide siguiente.

| Pregunta | Experimento | Respuesta |
|---|---|---|
| ¿Aprende sin conocimiento previo? | Experimento Base | NO — 51.2%, overfitting severo |
| ¿Ayuda el conocimiento preentrenado? | Transfer Learning | PARCIALMENTE — 70.5%, overfitting reducido |
| ¿El problema era el modelo o los datos? | Configuración Final | LOS DATOS — 91.6%, convergencia estable |

---

### NUEVA — "Qué cambia en la configuración final y por qué"
**Posición:** insertar después de slide 7 (Evolución del Rendimiento)

Diseño: tabla dos columnas. Fondo oscuro. Texto de cierre destacado en naranja o crema grande.

| Cambio | Problema que resolvía |
|---|---|
| Dataset reconstruido con tracking corregido | El modelo veía 5–10 "personas" distintas donde había solo 1 |
| AdamW en lugar de SGD | SGD ajustaba todos los pesos con la misma fuerza; AdamW calibra cada uno según su historial |
| Pose Jittering (σ=2px) | ViTPose tiene imprecisión inherente en coordenadas; el modelo debe ser robusto a esa variación |
| Label smoothing (ε=0.1) | Previene que el modelo sea excesivamente confiado en sus predicciones |

**Texto de cierre destacado:** "El salto de 70% → 92% no vino de un modelo más grande. Vino de entender por qué los datos eran incoherentes."

---

### NUEVA — "La comparación académica"
**Posición:** insertar después de slide 8 (Resultados por Clase)

Diseño: fondo oscuro. Columna "Este trabajo" remarcada en naranja. Datos exactos, no redondear.

| | Parmar et al. (2022) | Este trabajo |
|---|---|---|
| Estrategia | 2 clasificadores binarios | 1 clasificador multiclase |
| Dataset | Fitness-AQA | Fitness-AQA (mismo) |
| F1 — Codos | 0.45 | **0.91** |
| F1 — Rodillas | 0.84 | **0.90** |
| F1 — Global | — | **0.91** |

**Texto de cierre:** "Un clasificador unificado supera a dos clasificadores especializados — en ambas categorías."

---

### NUEVA — "Qué dice la matriz de confusión"
**Posición:** insertar después de la nueva slide "La comparación académica" (antes de Conclusiones)

Diseño: visual-first. La matriz de confusión (`assets/resultados/matriz_confusion.png`) ocupa la mayor parte del slide. Solo 3 anotaciones cortas al costado o debajo:

- "Diagonal alta → clasificación correcta en la mayoría de los casos"
- "Pocos errores cruzados entre las clases de error"
- "F1 similar en las tres clases → sin sesgo hacia la clase mayoritaria"

















---

## PARTE 2: CAMBIOS EN SLIDES EXISTENTES

### Slide 5 — "La Solución: El Pipeline"
En la sección inferior del slide donde describe ViTPose y PoseConv3D, **agregar** una línea de justificación a cada una:

- Bajo "ViTPose — Estimación de Poses": agregar "Por qué ViTPose: ve todas las articulaciones en relación desde el primer análisis, no parche por parche."
- Bajo "PoseConv3D — Clasificación Temporal": agregar "Por qué PoseConv3D: reutiliza arquitecturas de video consolidadas (ResNet3D) — misma capacidad que alternativas basadas en grafos, sin su complejidad."



---

### Slide 7 — "Evolución del Rendimiento del Modelo"
En la descripción de la columna "Configuración Final", **agregar** label smoothing a la lista de cambios. Reemplazar:

> "Dataset reconstruido + AdamW + Pose Jittering. F1-macro: 0.91. Brecha: 2–4%."

**Por:**

> "Dataset reconstruido + AdamW + Pose Jittering + Label smoothing (ε=0.1). F1-macro: 0.91. Brecha: 2–4%."

---

### Slide 8 — "Resultados por Clase"
**Eliminar** del bloque de texto de la izquierda todo lo referente a Parmar et al. — esa comparación pasa a la nueva slide dedicada. El texto que queda en el lado izquierdo es solo la descripción del dataset de evaluación (427 videos, Fitness-AQA).

**Eliminar** también la nota de diseño sobre `matriz_confusion.png` — la matriz pasa a la nueva slide dedicada.
