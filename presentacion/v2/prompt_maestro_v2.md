# Delta de actualización — PPT Defensa de Tesis
## Aplicar sobre el documento base (prompt_maestro_final.md)

---

## PARTE 1: SLIDES NUEVAS A INSERTAR

---

### NUEVA A — "¿Por qué ViTPose?"
**Posición:** insertar entre "La solución: el pipeline" y "ViTPose: estimación de poses"

- Diseño: dos columnas, visual-first, sin fórmulas
- Columna izquierda — "Otras herramientas (OpenPose, MediaPipe)":
  - Analizan la imagen en partes pequeñas, de forma local
  - Para conectar codo con hombro, necesitan combinar muchas piezas de información por separado
- Columna derecha — "ViTPose":
  - Ve todas las articulaciones en relación al mismo tiempo
  - Entiende de un vistazo cómo el codo se conecta con el hombro y la muñeca
- **Texto destacado en pantalla:** "ViTPose entiende el cuerpo como un todo, no como una suma de partes."
- Fondo oscuro. Minimalista.

---

### NUEVA B — "La lógica de los experimentos"
**Posición:** insertar antes de "Experimento base"

- Slide de transición que convierte los 3 experimentos en 3 preguntas encadenadas
- Diseño: diagrama de flujo o 3 columnas con flechas. Fondo oscuro. Texto conciso.

| Pregunta | Experimento | Respuesta |
|---|---|---|
| ¿Aprende sin conocimiento previo? | Experimento Base | NO — 51.2%, overfitting severo |
| ¿Ayuda el conocimiento preentrenado? | Transfer Learning | PARCIALMENTE — 70.5%, overfitting reducido |
| ¿El problema era el modelo o los datos? | Configuración Final | LOS DATOS — 91.6%, convergencia estable |

---

### NUEVA C — "Qué cambia en la configuración final y por qué"
**Posición:** insertar antes de "Configuración final"

- Tabla que explica cada cambio y el problema que resolvía
- Fondo oscuro. Texto de cierre destacado en naranja o crema grande.

| Cambio | Problema que resolvía |
|---|---|
| Dataset reconstruido con tracking corregido | El modelo veía 5–10 "personas" distintas donde había solo 1 |
| AdamW en lugar de SGD | SGD ajustaba todos los pesos con la misma fuerza; AdamW calibra cada uno según su historial |
| Pose Jittering (σ=2px) | ViTPose tiene imprecisión inherente en coordenadas; el modelo debe ser robusto a esa variación |
| Label smoothing (ε=0.1) | Previene que el modelo sea excesivamente confiado en sus predicciones |

**Texto de cierre destacado:** "El salto de 70% → 92% no vino de un modelo más grande. Vino de entender por qué los datos eran incoherentes."

---

### NUEVA D — "La comparación académica"
**Posición:** insertar después de "Comparación de experimentos"

- Slide dedicado a Parmar et al. (2022) — mismo dataset, estrategia diferente
- Fondo oscuro. Columna "Este trabajo" remarcada en naranja.

| | Parmar et al. (2022) | Este trabajo |
|---|---|---|
| Estrategia | 2 clasificadores binarios | 1 clasificador multiclase |
| Dataset | Fitness-AQA | Fitness-AQA (mismo) |
| F1 — Codos | 0.45 | **0.91** |
| F1 — Rodillas | 0.84 | **0.90** |
| F1 — Global | — | **0.91** |

**Texto de cierre:** "Un clasificador unificado supera a dos clasificadores especializados — en ambas categorías."

---

### NUEVA E — "Qué dice la matriz de confusión"
**Posición:** insertar después de "Resultados por clase"

- Visual-first: la matriz (`assets/resultados/matriz_confusion.png`) ocupa la mayor parte del slide
- Solo 3 anotaciones cortas al costado o debajo:
  - "Diagonal alta → clasificación correcta en la mayoría de los casos"
  - "Pocos errores cruzados entre las clases de error"
  - "F1 similar en las tres clases → sin sesgo hacia la clase mayoritaria"

---

## PARTE 2: CAMBIOS EN SLIDES EXISTENTES

---

### Slide "ViTPose: estimación de poses"
**Agregar** un bullet:
- "Por qué esta arquitectura: captura relaciones globales entre articulaciones desde el primer análisis — no parche por parche como las CNNs"

---

### Slide "PoseConv3D: clasificación temporal"
**Agregar** un bullet:
- "Por qué PoseConv3D: reutiliza directamente arquitecturas de video consolidadas (ResNet3D) — misma capacidad que alternativas basadas en grafos, menor complejidad operacional"

---

### Slide "Configuración final"
**Modificar** el primer bullet — reemplazar:
> "La clave: dataset reconstruido con tracking corregido + AdamW + Pose Jittering"

**Por:**
> "La clave: dataset reconstruido con tracking corregido + AdamW + Pose Jittering + Label smoothing (ε=0.1)"

---

### Slide "Resultados por clase"
**Eliminar** los dos últimos bullets:
- ~~Matriz de confusión: `assets/resultados/matriz_confusion.png`~~ → pasa a slide propia (NUEVA E)
- ~~Comparación con Parmar et al. (2022)...~~ → pasa a slide propia (NUEVA D)

El slide queda solo con la tabla de métricas por clase.
