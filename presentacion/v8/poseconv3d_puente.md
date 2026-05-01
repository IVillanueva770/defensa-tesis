# Propuesta: Bloque PoseConv3D
## Slides 33–39 del v8 — contenido literal para Gamma

---

## Contexto de dónde estamos

La slide 32 ya plantea la pregunta correcta: **"¿cómo entreno una IA que me evalúe la técnica?"**

Esa pregunta abre el bloque. Lo que sigue (slides 33–39) debe responderla en orden:

1. Por qué una CNN normal no alcanza → lleva naturalmente a PoseConv3D
2. Qué es PoseConv3D y qué lo hace especial
3. Los 3 experimentos de entrenamiento
4. La arquitectura final (slide 40 ya existe y está bien)

---

## SLIDE 33 — El problema del análisis por frame

> **Acción:** reemplazar el placeholder "Falta de acá en adelante" con este contenido.

**ETIQUETA (chip):** ENTRENAMIENTO

**TÍTULO:**
Una foto no alcanza

**LAYOUT:** dos columnas, imagen a la izquierda / texto a la derecha

**IMAGEN IZQUIERDA:**
Insertar el GIF de técnica correcta: `assets/videos_keypoints_superpuestos/gifs/79235_2_overlay_correct.gif`
(o cualquiera de los GIFs disponibles — el GIF es la demostración)

**TEXTO DERECHA (3 bullets):**
- El esqueleto en el frame 24 de un press correcto y uno incorrecto pueden verse igual
- La diferencia está en cómo se desarrolla el movimiento completo
- Necesitamos un modelo que "vea" 48 frames a la vez, no uno por uno

**ORADOR:**
"Ya tenemos los datos preparados: secuencias coherentes de 48 frames, un esqueleto por video, en el formato correcto. Ahora viene la pregunta clave: ¿qué modelo entrenamos sobre eso? Una CNN clásica, como las que vimos antes, analiza imágenes una por una. Si le muestro el frame 24 de un press correcto y el frame 24 de uno incorrecto, puede que sean prácticamente idénticos. El error no está en el momento — está en el recorrido. Necesitamos algo que vea el movimiento completo."

---

## SLIDE 34 — ¿Qué son las convoluciones 3D?

**ETIQUETA (chip):** ENTRENAMIENTO

**TÍTULO:**
De 2D a 3D: agregar el tiempo

**LAYOUT:** imagen central grande con leyenda debajo

**IMAGEN:**
`assets/imagenes_teoricas/2.8 tensorflow 3DCNN.png`

**LEYENDA DEBAJO DE LA IMAGEN:**
"El kernel no solo se desliza por el espacio — también avanza frame a frame"

**3 bullets debajo (o en columna lateral):**
- CNN 2D: kernel 3×3 sobre píxeles de un frame → detecta bordes, formas, texturas
- CNN 3D: kernel 3×3×3 sobre píxeles de varios frames → detecta patrones que evolucionan en el tiempo
- Resultado: el modelo aprende que los codos "se abren" en un movimiento incorrecto — no solo que están en cierta posición

**ORADOR:**
"Ya vimos convoluciones bidimensionales: un kernel que se desliza sobre la imagen y detecta patrones espaciales. La extensión tridimensional hace lo mismo, pero también sobre el eje del tiempo. El kernel procesa varios frames a la vez, y detecta cómo cambian los patrones de un frame al siguiente. Eso es exactamente lo que necesitamos: no saber dónde están los codos en el frame 24, sino cómo se movieron los codos a lo largo de los 48 frames del ejercicio."

---

## SLIDE 35 — PoseConv3D

> **Acción:** reemplazar el placeholder "PoseConv3D — {¿Qué es?...}" con esto.

**ETIQUETA (chip):** ENTRENAMIENTO

**TÍTULO:**
PoseConv3D: convoluciones 3D sobre esqueletos

**LAYOUT:** dos columnas

**COLUMNA IZQUIERDA — "Cómo funciona":**
- Input: 17 keypoints × 48 frames → mapa de calor por articulación por frame
- Apila esos mapas → tensor 3D
- Convoluciones 3D detectan patrones espacio-temporales en el esqueleto
- Output: 3 clases (Técnica Correcta / Error de Codos / Error de Rodillas)

**COLUMNA DERECHA — "Por qué esta arquitectura":**

| Alternativa | Limitación |
|---|---|
| CNN sobre frames | Sin memoria temporal |
| LSTM sobre coordenadas | Sin relaciones espaciales |
| **PoseConv3D** | **Ve espacio y tiempo juntos** |

**Una línea destacada al pie (grande):**
Arquitectura: ResNet3D SlowOnly — 12 millones de parámetros

**ORADOR:**
"PoseConv3D es la arquitectura que elegimos para el clasificador. Toma como entrada los mapas de calor de los 17 keypoints a lo largo de los 48 frames — básicamente, un cubo de datos donde cada capa temporal es un esqueleto completo. Una CNN clásica analiza frames aislados, perdiendo la información de cómo se mueve el cuerpo. Una LSTM puede ver la secuencia, pero trata los keypoints como números escalares, sin entender que el hombro y el codo están conectados. PoseConv3D combina los dos: ve las relaciones espaciales del esqueleto y cómo evolucionan en el tiempo. El backbone es ResNet3D SlowOnly, con doce millones de parámetros."

---

## SLIDE 36 — Tres experimentos, un camino

> **Acción:** reemplazar "Iteraciones sobre el entrenamiento de PoseConv3D — {Que cambios fui agregando en cada etapa}" con esto.

**ETIQUETA (chip):** RECORRIDO EXPERIMENTAL

**TÍTULO:**
Tres experimentos: el camino a 91.6%

**LAYOUT:** tres columnas o tres cajas horizontales, una por experimento

**CAJA 1:**
**Experimento Base**
Sin pesos preentrenados
→ 51.2%

**CAJA 2:**
**Transfer Learning**
Pesos de NTU RGB+D 60
→ 70.5%

**CAJA 3 (destacada en amarillo/acento):**
**Configuración Final**
Dataset corregido + AdamW + Jittering
→ 91.6%

**Una línea al pie:**
+40.4 puntos de mejora acumulada

**ORADOR:**
"Entrenamos el modelo en tres etapas. Cada una agrega algo sobre la anterior. El baseline nos da 51% — mejor que el azar, pero con overfitting severo. El transfer learning nos lleva a 70%, porque el modelo ya sabe cómo se mueve el cuerpo humano en general. Y la configuración final llega a 91.6%, principalmente por una razón: el dataset reconstruido con el algoritmo de tracking corregido. Veamos cada experimento."

---

## SLIDE 37 — Experimento Base

> **Acción:** reemplazar "Experimento Base — aca voy a tener que poner la arquitectura del modelo y etc, overfitting" con esto.

**ETIQUETA (chip):** RECORRIDO EXPERIMENTAL

**TÍTULO:**
Experimento 1: 51.2% — el modelo memoriza

**LAYOUT:** imagen central (curvas) + texto a la derecha

**IMAGEN:**
`assets/resultados/baseline_experimento_loss.png`

**TEXTO DERECHA:**
- Inicialización: pesos aleatorios — el modelo empieza sin saber nada de movimiento humano
- Resultado: 51.2% precisión (azar = 33.3%)
- Loss de training: ~0.07 → el modelo aprende de memoria los ejemplos
- Loss de validación: ~1.5+ → no generaliza a casos nuevos
- Brecha train/val: 46% → overfitting severo

**Destacado grande abajo:**
12 millones de parámetros, 1.708 videos de entrenamiento — demasiado modelo para tan pocos datos

**ORADOR:**
"Primer experimento: entrenamos desde cero, con pesos aleatorios. El modelo nunca vio movimiento humano antes. El resultado es 51%: mejor que el azar, así que el problema es learnable. Pero las curvas de pérdida cuentan la historia real: el training baja a 0.07 mientras que la validación sube a 1.5. La brecha es de 46 puntos. El modelo literalmente memorizó los 1.700 videos de entrenamiento en lugar de aprender a generalizar. Doce millones de parámetros sobre tan pocos datos garantizan overfitting."

---

## SLIDE 38 — Experimento 2: Transfer Learning

> **Acción:** reemplazar "Iteración 2: Transfer Learning + Fine Tunning" (actualmente vacío) con esto.

**ETIQUETA (chip):** RECORRIDO EXPERIMENTAL

**TÍTULO:**
Experimento 2: 70.5% — el modelo que ya sabe moverse

**LAYOUT:** imagen central (curvas) + texto a la derecha

**IMAGEN:**
`assets/resultados/experimento_250522_loss.png`

**TEXTO DERECHA:**
- Cambio clave: pesos preentrenados en **NTU RGB+D 60** (56.880 videos de acciones humanas)
- El modelo ya internalizó cómo se mueve el cuerpo antes de ver un solo overhead press
- Congelamiento de capas tempranas: preserva representaciones generales de movimiento
- Label smoothing ε=0.1: evita sobreconfianza en las predicciones
- Resultado: 70.5% (+19.3 pp sobre baseline)
- Brecha train/val: ~25% — overfitting reducido, pero aún presente

**ORADOR:**
"Segundo experimento: en lugar de empezar desde cero, inicializamos el modelo con pesos preentrenados en NTU RGB+D 60, un dataset con casi 57.000 videos de acciones humanas. La analogía es directa: es más fácil enseñarle a distinguir técnicas de press a alguien que ya sabe de movimiento humano que a alguien que nunca vio un cuerpo moverse. El salto es de 19 puntos — de 51% a 70%. Pero la brecha entre training y validación sigue siendo 25%. Los datos siguen siendo el problema."

---

## SLIDE 39 — Experimento 3: Configuración Final

> **Acción:** reemplazar "Iteración 3: Aumentación de Datos + AdamW" (actualmente vacío) con esto.

**ETIQUETA (chip):** RECORRIDO EXPERIMENTAL

**TÍTULO:**
Experimento 3: 91.6% — mejores datos, no modelo más complejo

**LAYOUT:** imagen central (curvas) + texto a la derecha

**IMAGEN:**
`assets/resultados/experimento_250525_loss.png`

**TEXTO DERECHA:**
- **Dataset reconstruido** con el algoritmo de tracking corregido — el cambio más importante
- AdamW: optimizador adaptativo, más estable que SGD para fine-tuning
- Pose Jittering (σ=2px): ruido gaussiano en coordenadas → robustez ante errores de detección
- CosineAnnealingLR: la tasa de aprendizaje baja suavemente hacia el final
- Resultado: **91.6%** — F1-Score macro: **0.91**
- Brecha train/val: **2–4%** — convergencia estable, sin overfitting

**Línea destacada al pie:**
El salto de 70% a 92% no vino de un modelo más sofisticado. Vino de datos correctos.

**ORADOR:**
"Tercer experimento. La diferencia principal no es el modelo — es que reconstruimos el dataset completo con el algoritmo de corrección de tracking. Ahora el modelo recibe secuencias coherentes de 48 frames de una sola persona. Agregamos AdamW, jittering de poses y un scheduler cosenoidal. El resultado: 91.6%, con una brecha de solo 2 a 4 puntos entre training y validación. Las curvas convergen limpiamente. El mensaje es que el salto de 21 puntos no vino de arquitectura más compleja — vino de datos de mejor calidad."

---

## Notas sobre la slide 40 — Arquitectura final

La slide 40 ya tiene el diagrama del pipeline completo y está bien. No cambiar.

Después del Experimento 3 (slide 39) hay dos opciones:
- **Opción A (recomendada):** ir directo a slide 40 "Arquitectura final" como cierre visual del bloque de entrenamiento antes de pasar a Resultados
- **Opción B:** agregar una slide de tabla comparativa de los 3 experimentos antes de la arquitectura

Si el tiempo lo permite, la tabla vale la pena — el jurado la va a agradecer. Sería:

| | Exp. Base | Transfer Learning | Config. Final |
|---|---|---|---|
| Precisión | 51.2% | 70.5% | **91.6%** |
| F1-Score | 0.48 | 0.69 | **0.91** |
| Brecha train/val | 46% | 25% | 2–4% |

**Una sola frase para decir:** "Cuarenta puntos de mejora en tres experimentos."

---

## Resumen del bloque — qué va dónde

| Slide | Título propuesto | Estado |
|---|---|---|
| 32 | "Ahora, ¿cómo entreno una IA?" | Ya existe, correcto |
| 33 | "Una foto no alcanza" | Reemplazar placeholder |
| 34 | "De 2D a 3D: agregar el tiempo" | Reemplazar placeholder |
| 35 | "PoseConv3D: convoluciones 3D sobre esqueletos" | Reemplazar placeholder |
| 36 | "Tres experimentos: el camino a 91.6%" | Reemplazar placeholder |
| 37 | "Experimento 1: 51.2% — el modelo memoriza" | Reemplazar placeholder |
| 38 | "Experimento 2: 70.5% — el modelo que ya sabe moverse" | Llenar vacío |
| 39 | "Experimento 3: 91.6% — mejores datos, no modelo más complejo" | Llenar vacío |
| 40 | Arquitectura final | Ya existe, correcto |

---

## Sobre las slides de Resultados y Discusión (42–43)

Esas también tienen placeholders con tus notas. Cuando termines el bloque de entrenamiento, avísame y las completamos juntos — ya tengo los números exactos.
