# Contenido de slides — v7
## Ignacio Villanueva | UCASAL 2026

**Cómo leer este archivo:**
- **SLIDE:** lo que va en la diapositiva (texto literal, layout, imagen)
- **ORADOR:** lo que se dice en voz alta (no va en la diapo)

---

## SLIDE 11 — ELIMINAR ESTA DIAPOSITIVA

---

## SLIDE 12 — Dataset

**Título:** 2.135 videos etiquetados de press de hombro

**Layout:** 3 bloques/columnas en el centro

| Bloque 1 | Bloque 2 | Bloque 3 |
|---|---|---|
| Técnica correcta | Error de codos | Error de rodillas |
| ~900 videos | ~650 videos | ~585 videos |
| 42% | 30% | 28% |

**Texto pequeño al pie:** Dataset Fitness-AQA — Parmar et al. (2022)

---

**ORADOR:** Mientras investigaba la literatura, encontré el paper de Parmar et al. que trabajaba exactamente el mismo ejercicio con el mismo problema. Les mandé un email directamente y me reenviaron el dataset. Eso también me permitió comparar mis resultados contra un benchmark publicado, que es lo que vamos a ver al final.

---

## SLIDE 13 — Computer Vision para estimación de poses

**Título:** ¿Cómo ve una computadora el cuerpo humano?

**Layout:** dos columnas con flecha entre ellas + imagen a la derecha (o abajo)

**Columna izquierda:**
- Etiqueta: IMAGEN RGB
- "1.920 × 1.080 valores de color por frame"

**Flecha →**

**Columna derecha:**
- Etiqueta: POSE ESTIMADA
- "17 coordenadas (x, y) por frame"

**Imagen:** diagrama COCO de 17 keypoints
`assets/imagenes_teoricas/2.5 keypoints COCO diagram.png`

**Texto al pie (pequeño):** Nariz · Ojos · Orejas · Hombros · Codos · Muñecas · Caderas · Rodillas · Tobillos

---

**ORADOR:** En lugar de analizar píxeles — que no nos dicen nada sobre si alguien está haciendo bien un ejercicio — abstraemos el cuerpo humano a 17 puntos articulares. Eso es el estándar COCO: 17 coordenadas por frame. Mucho más compacto y biomecánicamente significativo.

---

## SLIDE 14 — ViTPose (concepto)

**Título:** ViTPose: detecta el esqueleto frame a frame

**Layout:** imagen grande a la derecha, texto a la izquierda

**Texto izquierda (3 puntos cortos):**
- CNN: detecta patrones locales. La información viaja capa por capa.
- Vision Transformer: divide la imagen en parches de 16×16 px y los procesa todos a la vez.
- ViTPose: usa esa arquitectura para estimar los 17 keypoints del cuerpo.

**Tag destacado (caja o etiqueta):**
Top-down: YOLOv8 detecta la persona → ViTPose estima la pose dentro de ese recorte

**Imagen:** `assets/imagenes_teoricas/2.4 Dosovitskiy ViT architecture.png`

---

**ORADOR:** La ventaja de los Vision Transformers sobre las CNN clásicas es que desde la primera capa, cualquier parte de la imagen puede relacionarse con cualquier otra. Si el modelo ve el hombro, puede inferir inmediatamente dónde debería estar el codo, sin esperar a que esa información suba capa por capa.

---

## SLIDE 15 — Implementación de ViTPose

**Título:** ViTPose en la práctica

**Layout:** GIF grande a la izquierda (ocupa mitad de slide), texto a la derecha

**Texto derecha (bullets):**
- Modelo: ViT-B — 133 keypoints por persona
- Detector: YOLOv8-s
- Infraestructura: Google Colab (GPU gratuita)
- Procesado en lotes de ~600 videos por sesión
- Output: 1 archivo JSON por video

**Imagen/GIF izquierda:**
`assets/videos_keypoints_superpuestos/gifs/79235_2_overlay_correct.gif`

---

**ORADOR:** Acá ya pueden ver el resultado: el esqueleto detectado frame a frame sobre el video real. Cada punto es uno de los 17 keypoints COCO, con su coordenada y su nivel de confianza.

---

## SLIDE 16 — De ViTPose a PoseConv3D

**Título:** Transformar el esqueleto en datos de entrenamiento

**Layout:** diagrama de flujo horizontal con 3 bloques y flechas

**Bloque 1:**
- Etiqueta: SALIDA DE VITPOSE
- "JSON"
- "133 keypoints × N personas × M frames"

**→**

**Bloque 2 (proceso, texto más pequeño):**
- Seleccionar 17 keypoints COCO
- Identificar el sujeto principal
- Normalizar a 48 frames
- Convertir a formato pickle

**→**

**Bloque 3:**
- Etiqueta: ENTRADA DE POSECONV3D
- "Pickle"
- "17 keypoints × 1 persona × 48 frames"

**Texto destacado al pie (caja o color diferente):**
Problema descubierto: ViTPose no recuerda entre frames. Los IDs de personas cambian entre frames consecutivos.

---

**ORADOR:** La transformación parece mecánica, pero ahí dentro apareció el problema técnico más importante del proyecto. ViTPose procesa cada frame de forma completamente independiente — no tiene memoria. Y eso causó que los IDs de las personas cambiaran entre frames. Se los muestro en las próximas tres diapositivas.

---

## SLIDE 17 — Preprocesamiento: Iteración 1

**Título:** Iteración 1: quedarse con la persona más grande

**Layout:** dos columnas

**Columna izquierda — EL ENFOQUE:**
En cada frame, seleccionar la persona con el bounding box de mayor área.

**Columna derecha — EL PROBLEMA:**
En algunos videos, alguien más cerca de la cámara tiene un bounding box más grande que quien está ejercitando.

**Texto al pie (destacado):**
Resultado: el modelo entrena con keypoints mezclados de personas distintas.

---

**ORADOR:** La intuición era simple: el sujeto principal probablemente ocupa más espacio en la imagen. Pero no siempre es así. El ángulo de la cámara puede hacer que un espectador en el fondo se vea más grande. Y en esos casos, el modelo estaba aprendiendo sobre la persona equivocada.

---

## SLIDE 18 — Preprocesamiento: Iteración 2

**Título:** Iteración 2: guardar todos... pero los IDs cambian

**Layout:** línea de tiempo o secuencia de frames con etiquetas

**Secuencia de frames (visual central):**

```
Frame 18        Frame 20         Frame 21
  ID 44 ✓        ID 44 ✗         ID 51 ← misma persona
                (no detectado)
```

**Texto destacado debajo:**
El modelo interpreta esto como 3 personas distintas en lugar de 1 secuencia continua.

**Texto pequeño al pie:**
Causa: ViTPose procesa cada frame de forma independiente — no hay tracking entre frames.

---

**ORADOR:** El ID 44 desaparece dos frames por una oclusión parcial, y cuando reaparece, ViTPose le asigna el ID 51. Son la misma persona física, pero el modelo no lo sabe. En lugar de recibir una secuencia continua de 48 frames de un mismo sujeto, recibe fragmentos discontinuos. No puede aprender el movimiento completo.

---

## SLIDE 19 — Preprocesamiento: Iteración 3

**Título:** Iteración 3: algoritmo propio de corrección de tracking

**Layout:** la regla destacada en el centro, before/after abajo

**Caja central (texto grande o prominente):**
Si la persona desaparece ≤ 3 frames consecutivos
y reaparece a ≤ 25 píxeles de distancia
→ se mantiene el ID original

**Número grande debajo de la regla:**
87% de las discontinuidades corregidas

**Visual before/after (debajo o al costado):**
- ANTES:  `[ID 44 ████████████████]` · gap · `[ID 51 ████████████████████████████]`
- DESPUÉS: `[ID 44 ████████████████████████████████████████████████]`

---

**ORADOR:** Tres frames de tolerancia para oclusiones breves, 25 píxeles para movimiento natural sin confundir dos personas distintas. Umbrales establecidos empíricamente. Esta corrección fue determinante — el salto de 70% a 92% de precisión no habría sido posible sin secuencias coherentes.

---

## SLIDE 20 — "~60% del trabajo" (no tocar)

---

## SLIDE 21 — PoseConv3D

**Título:** PoseConv3D: el clasificador que ve el ejercicio entero

**Layout:** imagen a la izquierda (grande), texto a la derecha

**Texto derecha (bullets):**
- CNN clásica: analiza 1 imagen → 1 predicción
- PoseConv3D: analiza 48 frames → 1 predicción
- No opera sobre píxeles — opera sobre los heatmaps de los 17 keypoints
- Detecta patrones espacio-temporales: cómo se mueve cada articulación a lo largo del tiempo

**Tag o caja al pie:**
ResNet3D SlowOnly · ~12M parámetros · 3 clases de salida

**Imagen:** `assets/imagenes_teoricas/2.8 tensorflow 3DCNN.png`

---

**ORADOR:** La diferencia clave con una red que analiza fotos: PoseConv3D ve el movimiento completo. Una foto a mitad de un overhead press correcto e incorrecto puede parecer igual. La diferencia está en cómo se desarrolla la secuencia. Las convoluciones 3D deslizan simultáneamente sobre el espacio y el tiempo.

---

## SLIDE 22 — Experimento 1: Baseline

**Título:** Experimento 1: entrenamiento desde cero

**Etiqueta de sección:** RECORRIDO EXPERIMENTAL · 1 de 3

**Layout:** gráficas izquierda, métricas y diagnóstico derecha

**Gráficas izquierda:**
`[PLACEHOLDER: assets/resultados/baseline_experimento_loss.png]`
`[PLACEHOLDER: assets/resultados/baseline_experimento_accuracy.png]`

**Texto derecha:**

Configuración:
- Inicialización aleatoria (desde cero)
- Optimizador: SGD · lr=0.05 · momentum=0.9

Resultado:
- **Precisión: 51.2%** (azar = 33.3%)
- F1-Score: 0.48
- Training: 97.5% · Validación: 51.2% · Brecha: 46%

Diagnóstico:
- 12M de parámetros, 1.708 videos de entrenamiento
- El modelo memoriza en lugar de generalizar

---

**ORADOR:** El modelo alcanzó 97% en training y 51% en validación — eso es overfitting severo. Las curvas de pérdida divergen de forma contundente. Pero el 51% nos dice algo importante: el problema es learnable. Solo necesitamos mejor punto de partida.

---

## SLIDE 23 — Experimento 2: Transfer Learning

**Título:** Experimento 2: el modelo que ya sabe moverse

**Etiqueta de sección:** RECORRIDO EXPERIMENTAL · 2 de 3

**Layout:** gráficas izquierda, cambios y métricas derecha

**Gráficas izquierda:**
`[PLACEHOLDER: assets/resultados/experimento_250522_loss.png]`
`[PLACEHOLDER: assets/resultados/experimento_250522_accuracy.png]`

**Texto derecha:**

Cambios aplicados:
- Pesos preentrenados en NTU RGB+D 60 (56.880 videos de acciones humanas)
- Capas tempranas congeladas durante el fine-tuning
- Label smoothing ε=0.1: etiquetas [0.9, 0.05, 0.05] en lugar de [1, 0, 0]

Resultado:
- **Precisión: 70.5%** (+19.3pp)
- F1-Score: 0.69
- Brecha training/val: 25%

---

**ORADOR:** Inicializar con pesos preentrenados en 56.000 videos de movimiento humano le da al modelo un punto de partida mucho mejor. El label smoothing evita predicciones sobreconfiadas. La brecha bajó de 46% a 25%, pero sigue siendo alta. Los datos siguen siendo el problema.

---

## SLIDE 24 — Experimento 3: Configuración Final

**Título:** Experimento 3: mejores datos, no modelo más complejo

**Etiqueta de sección:** RECORRIDO EXPERIMENTAL · 3 de 3

**Layout:** gráficas izquierda, cambios y métricas derecha

**Gráficas izquierda:**
`[PLACEHOLDER: assets/resultados/experimento_250525_loss.png]`
`[PLACEHOLDER: assets/resultados/experimento_250525_accuracy.png]`

**Texto derecha:**

Cambios aplicados:
- **Dataset reconstruido con tracking corregido** ← el cambio más impactante
- AdamW: tasa de aprendizaje adaptativa por parámetro
- Pose Jittering (σ=2px): ruido gaussiano en coordenadas de keypoints
- CosineAnnealingLR: decaimiento suave de la tasa de aprendizaje

Resultado:
- **Precisión: 91.6%** (+21.1pp)
- F1-Score: 0.91
- Brecha training/val: 2–4%

---

**ORADOR:** El salto de 70% a 92% no vino de un modelo más sofisticado. Vino de que los datos de entrada finalmente eran correctos — secuencias coherentes de una sola persona durante los 48 frames. El algoritmo de tracking fue la palanca decisiva.

---

## SLIDE 25 — Comparación de los tres experimentos

**Título:** El progreso en tres pasos

**Layout:** tabla grande y centrada, número grande abajo

**Tabla:**

|  | Exp. Base | Transfer Learning | Config. Final |
|---|---|---|---|
| Precisión | 51.2% | 70.5% | **91.6%** |
| F1-Score | 0.48 | 0.69 | **0.91** |

**Número grande debajo (destacado en color de acento):**
+40.4 puntos porcentuales desde el baseline

---

**ORADOR:** Tres experimentos, tres decisiones distintas. El transfer learning fue el salto de conocimiento. La corrección de datos fue el salto de calidad.

---

## SLIDE 26 — Resultados detallados

**Título:** Un clasificador, mejor que dos especializados

**Layout:** tabla izquierda + matriz de confusión derecha arriba + comparación derecha abajo

**Tabla izquierda — métricas por clase:**

| Clase | Precision | Recall | F1 |
|---|---|---|---|
| Técnica Correcta | 0.94 | 0.92 | 0.93 |
| Error de Codos | 0.90 | 0.92 | 0.91 |
| Error de Rodillas | 0.89 | 0.91 | 0.90 |
| **Macro avg** | **0.91** | **0.92** | **0.91** |

**Imagen derecha arriba:**
`[PLACEHOLDER: assets/resultados/matriz_confusion.png]`

**Texto derecha abajo — comparación con literatura:**

Parmar et al. (2022) — 2 clasificadores binarios:
- F1 codos: 0.45 · F1 rodillas: 0.84

Este trabajo — 1 clasificador multiclase:
- F1 codos: 0.91 · F1 rodillas: 0.90

---

**ORADOR:** El modelo es balanceado — no favorece ninguna clase. Y al comparar con el paper de referencia, que usó dos clasificadores especializados separados sobre el mismo dataset: un único modelo multiclase los supera en ambas categorías.

---

## SLIDE 27 — Conclusiones

**Título:** Lo que se logró

**Layout:** 5 bullets con ícono o número adelante

- Pipeline completo: video crudo → evaluación de técnica. Documentado y reproducible.
- Precisión: 91.6% · F1-Score macro: 0.91
- Contribución original: algoritmo de corrección de tracking (87% de discontinuidades resueltas)
- Costo de software: $0 — alternativa a sistemas de USD $10.000–$100.000
- Base metodológica replicable a otros ejercicios

---

**ORADOR:** Los cuatro objetivos específicos del trabajo están cumplidos. El pipeline funciona, está documentado y es reproducible con hardware estándar.

---

## SLIDE 28 — Trabajo futuro

**Título:** ¿Hacia dónde puede crecer?

**Layout:** 5 bullets

- Más categorías de error: trayectoria de la barra, activación del core, posición de los pies
- Localización temporal del error: señalar en qué momento del movimiento ocurre
- Expansión a otros ejercicios: sentadilla, peso muerto, press de banca
- Integración con LLMs para feedback correctivo en lenguaje natural
- Validación con entrenadores y practicantes reales

---

**ORADOR:** La metodología está validada. El siguiente paso natural es ampliarla — más ejercicios, más tipos de error, y eventualmente feedback en lenguaje natural para el practicante.

---

## SLIDE 29 — Cierre personal

**Título:** (ninguno, o solo "Gracias")

**Layout:** imagen grande (ocupa la mayor parte del slide), texto pequeño al pie

**Imagen:**
`[PLACEHOLDER: frame del video personal en Corea — assets/personal/video mio en corea mientras investigaba.mp4]`

**Texto al pie:**
UCASAL → Universidad de Cádiz → POSTECH → acá.

**Texto de agradecimientos (pequeño, discreto):**
A la familia, a Agustina, a los amigos, a Lorena, a los que hicieron posibles los intercambios, y a UCASAL.

---

**ORADOR:** Arranqué este proyecto con conocimientos básicos de IA y terminé implementando un sistema con resultados publicables, pasando por dos continentes. Gracias.
