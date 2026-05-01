# Recomendaciones de contenido — v6 presentación

## Ignacio Villanueva | UCASAL 2026

**Qué es este archivo:** recomendaciones slide por slide para completar la presentación v5 en Gamma. No es texto literal para copiar — es la información que debe estar presente y cómo contarla. Los números y métricas son exactos y no se inventan.

**Estructura:** las slides 1–10 están finalizadas. La slide 11 (meta-instrucción) se elimina. Las slides 12–19 se llenan con lo que sigue. La slide 20 no se toca. Las slides 21–28 son nuevas.

---

## SLIDE 11 — ELIMINAR

Esta slide es una nota interna. Eliminarla de la presentación final.

---

**Qué es este archivo:** recomendaciones slide por slide para completar la presentación v5 en Gamma. No es texto literal para copiar — es la información que debe estar presente y cómo contarla. Los números y métricas son exactos y no se inventan.


## SLIDE 12 — Obtención del dataset

**Título sugerido:** "2.135 videos etiquetados de press de hombro"

**Idea central:** el dataset provino de contactar directamente a los autores del paper de referencia.

**Qué poner:**
- **Historia para contar oralmente:** al investigar la literatura, encontré el paper de Parmar et al. (2022) — trabajan exactamente el mismo ejercicio, con el mismo problema. Les mandé un email directamente y me reenviaron el dataset Fitness-AQA.
- **El dataset en números:**
  - 2.135 videos MP4 de press de hombro
  - 3 categorías: Técnica correcta (~900 videos, 42%), Error de codos (~650, 30%), Error de rodillas (~585, 28%)
  - Clips procesados en ventanas de 48 frames para entrenamiento
- **Por qué este y no otro:** permite comparar resultados contra un benchmark publicado — clave para la discusión final

**Visual:** tres bloques o columnas con el nombre de cada categoría y su número, bien grande. Sin texto corrido.

---

## SLIDE 13 — Computer Vision para estimación de Poses Humanas

**Título sugerido:** "¿Cómo ve una computadora el cuerpo humano?"

**Idea central:** en lugar de analizar píxeles, abstraemos el cuerpo humano a 17 puntos anatómicos.

**Puente básico → complejo:**
- **Básico:** Computer Vision enseña a las computadoras a extraer significado de imágenes. Una imagen RGB es solo una matriz de números — valores de rojo, verde y azul por píxel.
- **El problema:** para evaluar si alguien ejecuta bien un ejercicio, los píxeles no ayudan directamente. Necesitamos saber *dónde están las articulaciones*.
- **La solución:** representar el cuerpo como 17 puntos clave (formato estándar COCO): nariz, ojos, orejas, hombros, codos, muñecas, caderas, rodillas, tobillos.
- **El beneficio:** en vez de procesar 1.920×1.080 valores de color por frame, trabajamos con 17 coordenadas (x, y, confianza). Mucho más compacto y biomecánicamente significativo.

**Visual:** el diagrama COCO de 17 keypoints. Si el diseño lo permite, side-by-side: frame de video crudo vs. esqueleto superpuesto.

**Asset:** `assets/imagenes_teoricas/2.5 keypoints COCO diagram.png`

---

## SLIDE 14 — ViTPose (concepto)

**Título sugerido:** "ViTPose: el ojo que detecta el esqueleto"

**Idea central:** ViTPose usa Vision Transformers para capturar relaciones globales entre articulaciones desde el primer momento.

**Puente básico → complejo:**
- **Básico (CNN):** las redes convolucionales detectan patrones locales: bordes → formas → objetos. Para saber dónde está el codo, la información tiene que "viajar" capa por capa desde el hombro.
- **La evolución:** los Transformers (originalmente para texto — como GPT) procesan secuencias viendo todos los elementos a la vez. Si dividimos una imagen en parches de 16×16 píxeles, la podemos tratar como una secuencia de "palabras" y aplicar el mismo mecanismo.
- **ViT (Vision Transformer):** hace exactamente eso. Desde la primera capa, un parche puede "atender" a cualquier otro parche de la imagen, sin importar la distancia.
- **ViTPose:** aplica ViT a estimación de poses. La ventaja clave: si el modelo ve el hombro, puede inferir inmediatamente dónde debería estar el codo — sin esperar a que la información "suba" capa por capa.
- **Enfoque top-down:** primero YOLOv8 detecta a la persona (bounding box), después ViTPose estima los 17 keypoints dentro de ese recorte.

**Visual:** el diagrama de la arquitectura ViT.

**Asset:** `assets/imagenes_teoricas/2.4 Dosovitskiy ViT architecture.png`

---

## SLIDE 15 — Implementación de ViTPose

**Título sugerido:** "ViTPose en la práctica: 2.135 videos procesados"

**Idea central:** cómo se implementó concretamente, con el resultado visible.

**Qué poner:**
- **Herramienta:** easy_ViTPose sobre Google Colab (GPU gratuita)
- **Configuración:**
  - Modelo: ViT-B (base) con COCO wholebody → 133 keypoints por persona
  - Detector de personas: YOLOv8-s
- **Restricción operativa:** se procesó en lotes de ~600 videos por sesión de Colab (límite de la GPU gratuita)
- **Output:** un archivo JSON por video, con keypoints frame a frame y valor de confianza por punto
- **La demostración:** un GIF con el esqueleto superpuesto sobre el video real. Habla por sí solo.

**Visual:** uno de los GIFs de keypoints superpuestos (técnica correcta preferiblemente).

**Assets:**
- `assets/videos_keypoints_superpuestos/gifs/79235_2_overlay_correct.gif`
- `assets/videos_keypoints_superpuestos/gifs/79540_1_overlay_correct.gif`

---

## SLIDE 16 — De ViTPose a PoseConv3D

**Título sugerido:** "El puente: de 133 puntos por frame a datos de entrenamiento"

**Idea central:** la salida de ViTPose necesita transformarse para ser entrada de PoseConv3D — y en ese proceso apareció el problema técnico más importante del proyecto.

**Qué poner:**
- **Qué da ViTPose:** JSON con 133 keypoints × N personas × M frames (variable)
- **Qué necesita PoseConv3D:** pickle con 17 keypoints COCO × 1 persona × exactamente 48 frames
- **Transformaciones necesarias:** seleccionar 17 de los 133 keypoints / identificar el sujeto principal / normalizar a 48 frames / convertir formato
- **El problema inesperado:** ViTPose procesa cada frame de forma independiente — sin memoria entre frames. Los IDs de personas cambian entre frames. → Les cuento cómo lo resolví en los próximos tres slides.

**Visual:** diagrama simple de flujo:
`JSON (133 kp × N personas × M frames)` → `[procesamiento]` → `pickle (17 kp × 1 persona × 48 frames)`

Puede ser minimalista: flechas y cajitas.

---

## SLIDE 17 — Preprocesamiento: Iteración 1

**Título sugerido:** "Intento 1: la persona más grande en cada frame"

**Idea central:** la heurística más simple falló — la persona más grande no siempre es quien hace el ejercicio.

**Qué poner:**
- **Enfoque:** en cada frame, seleccionar la persona con el bounding box de mayor área
- **Intuición:** el sujeto principal probablemente ocupa más espacio en la imagen
- **Problema descubierto:** en algunos videos, alguien en segundo plano (más cerca de la cámara) aparece con bounding box más grande que el sujeto que está ejercitando
- **Consecuencia:** el dataset mezcla keypoints de personas distintas frame a frame. El modelo aprende ruido, no patrones.

**Visual:** esquema conceptual simple: frame con dos personas, indicando cuál queda seleccionada (equivocada) y cuál debería ser. Sin código ni fórmulas.

---

## SLIDE 18 — Preprocesamiento: Iteración 2

**Título sugerido:** "Intento 2: guardar todos... pero los IDs cambian"

**Idea central:** ViTPose no recuerda entre frames — la misma persona puede aparecer con IDs distintos.

**Qué poner:**
- **Nuevo enfoque:** mantener todas las personas detectadas por frame, sin filtro
- **Problema:** ViTPose procesa cada frame de forma independiente. Si una persona desaparece brevemente (oclusión parcial) y reaparece, le asigna un ID nuevo.
- **Ejemplo concreto del proyecto** (real, video 62794_6):
  - Frame 18: Persona **ID 44** visible
  - Frame 20: Persona ID 44 **no detectada** (oclusión breve)
  - Frame 21: Aparece Persona **ID 51** — en exactamente la misma posición que ID 44
  - → Misma persona física, ID diferente
- **Consecuencia:** el modelo recibe secuencias fragmentadas en vez de 48 frames continuos. No puede aprender el movimiento completo.

**Visual:** línea de tiempo simple:

```
Frame 18: ID 44 ✓ → Frame 20: ✗ → Frame 21: ID 51 ❓
                              "misma persona, ID diferente"
```

---

## SLIDE 19 — Preprocesamiento: Iteración 3 — Corrección de Tracking

**Título sugerido:** "Solución propia: algoritmo de corrección de tracking"

**Idea central:** una regla geométrica simple corrige el 87% de los IDs rotos.

**Qué poner:**
- **La regla:**
  - Si una persona desaparece durante **≤ 3 frames consecutivos**
  - Y reaparece a una distancia euclidiana promedio de **≤ 25 píxeles** de donde estaba
  - → Se mantiene el ID original (es la misma persona)
- **Por qué estos umbrales:** 3 frames tolera oclusiones breves; 25px permite movimiento natural sin confundir a dos personas distintas
- **Resultado:** 87% de las discontinuidades corregidas en validación
- **Efecto:** el modelo ahora recibe secuencias coherentes de 48 frames de un mismo sujeto
- **Por qué importa:** esta es la contribución técnica original del proyecto. Fue determinante para pasar de 70% a 92% de precisión.

**Visual:** diagrama before/after:

```
ANTES:  [ID 44: frames 1–18] | GAP | [ID 51: frames 21–48]  ← fragmentado
DESPUÉS: [ID 44: frames 1–48]                               ← continuo
```

---

## SLIDE 20 — "~60% del trabajo" (no tocar)

Ya está bien. No cambiar.

---

## SLIDE 21 — PoseConv3D: clasificación del movimiento completo

**Título sugerido:** "PoseConv3D: el clasificador que ve el ejercicio entero"

**Idea central:** a diferencia de una CNN que analiza fotos, PoseConv3D analiza movimientos completos a lo largo del tiempo.

**Puente básico → complejo:**
- **Básico:** una red neuronal clásica clasifica imágenes individuales (foto de un gato → "gato")
- **El problema para ejercicios:** una foto a mitad de un overhead press correcto e incorrecto pueden parecer similares. La diferencia está en cómo se desarrolla el movimiento completo.
- **La solución — convoluciones 3D:** en lugar de detectar patrones en 2D (espacio), los detectan en 3D (espacio + tiempo). El kernel desliza simultáneamente sobre el espacio y los frames consecutivos.
- **PoseConv3D específicamente:** no opera sobre píxeles de video, sino sobre heatmaps de keypoints. Para cada frame genera un mapa de probabilidades 2D por cada uno de los 17 keypoints → los apila → tensor 3D → convoluciones 3D.
- **Input:** 48 frames × 17 keypoints
- **Output:** 3 clases (Técnica Correcta / Error de Codos / Error de Rodillas)
- **Arquitectura:** ResNet3D SlowOnly, ~12 millones de parámetros

**Visual:** el diagrama de CNN 3D.

**Asset:** `assets/imagenes_teoricas/2.8 tensorflow 3DCNN.png`

---

## SLIDE 22 — Experimento 1: entrenamiento desde cero

**Título:** "Experimento 1: 51.2% — el modelo memoriza, no aprende"

**Cambios aplicados y qué significan:**
- **Inicialización aleatoria (desde cero):** el modelo no sabe nada de movimiento humano al empezar. Todo se aprende de los 1.708 videos de training.

**Configuración:**
- Optimizador: SGD, lr=0.05, momentum=0.9
- Augmentación: flip horizontal + RandomResizedCrop
- Sin preentrenamiento, sin regularización avanzada

**Resultado:**
- Precisión validación: **51.2%** (referencia: azar = 33.3% para 3 clases)
- F1-Score: **0.48**
- Precisión training: **97.5%** → brecha training/val: **46%** → overfitting severo
- Loss training: ~0.07 / Loss validación: ~1.5+ → curvas divergen

**El diagnóstico:** 12 millones de parámetros aprendiendo de solo 1.708 videos → el modelo memoriza los ejemplos de entrenamiento en lugar de generalizar patrones.

**Lo que nos dice:** el problema es learnable (51% > 33%), pero necesitamos mejor punto de partida y regularización.

**Visual:** las curvas de pérdida divergentes son la imagen más contundente de este slide.

**Assets:**
- `[PLACEHOLDER: assets/resultados/baseline_experimento_loss.png]`
- `[PLACEHOLDER: assets/resultados/baseline_experimento_accuracy.png]`

---

## SLIDE 23 — Experimento 2: transfer learning

**Título:** "Experimento 2: 70.5% — el modelo que ya sabe moverse"

**Cambios aplicados y qué significan:**
1. **Pesos preentrenados en NTU RGB+D 60** (56.880 videos de acciones humanas): el modelo ya internalizó cómo se mueve el cuerpo humano en general. Analogía: es más fácil enseñarle a distinguir técnicas de press a alguien que ya sabe de movimiento humano que a alguien que parte de cero.
2. **Congelamiento de capas tempranas (frozen_stages=2):** las capas con representaciones genéricas de movimiento se preservan; solo se re-entrenan las capas superiores más específicas. Evita sobreescribir conocimiento útil con pocos datos.
3. **Label smoothing (ε=0.1):** en vez de etiquetas perfectas [1, 0, 0], se usa [0.9, 0.05, 0.05]. Evita predicciones sobreconfiadas y actúa como regularizador.

**Resultado:**
- Precisión validación: **70.5%** (+19.3pp sobre baseline)
- F1-Score: **0.69**
- Brecha training/val: **~25%** (reducida desde 46%, pero aún presente)
- Las curvas ya no divergen tan agresivamente

**El mensaje:** el transfer learning fue la palanca más importante en términos de conocimiento previo. Pero el 25% de brecha nos dice que los datos siguen siendo el problema.

**Assets:**
- `[PLACEHOLDER: assets/resultados/experimento_250522_loss.png]`
- `[PLACEHOLDER: assets/resultados/experimento_250522_accuracy.png]`

---

## SLIDE 24 — Experimento 3: configuración final

**Título:** "Experimento 3: 91.6% — mejores datos, no modelo más complejo"

**Cambios aplicados y qué significan:**
1. **Dataset reconstruido con tracking corregido:** el cambio más impactante. Las secuencias ahora son coherentes — el modelo ve el ejercicio completo de una sola persona, no secuencias fragmentadas de IDs distintos.
2. **AdamW** (en lugar de SGD): optimizador adaptativo que ajusta la tasa de aprendizaje por parámetro. Más estable que SGD con tasa fija, especialmente en fine-tuning.
3. **Pose Jittering (σ=2px):** agrega ruido gaussiano pequeño a las coordenadas de los keypoints durante el training. El modelo aprende a ser robusto ante pequeños errores de detección — data augmentation específico para poses.
4. **CosineAnnealingLR:** la tasa de aprendizaje baja suavemente siguiendo una curva cosenoidal. Mejor convergencia al final del entrenamiento.

**Resultado:**
- Precisión validación: **91.6%** (+21.1pp sobre Exp. 2, +40.4pp sobre baseline)
- F1-Score: **0.91**
- Brecha training/val: **2–4%** — convergencia estable, sin overfitting
- Las curvas convergen limpias

**El mensaje del slide:** el salto de 70% a 92% no vino de un modelo más sofisticado. Vino de que los datos de entrada finalmente eran correctos. El algoritmo de tracking fue la palanca decisiva.

**Assets:**
- `[PLACEHOLDER: assets/resultados/experimento_250525_loss.png]`
- `[PLACEHOLDER: assets/resultados/experimento_250525_accuracy.png]`

---

## SLIDE 25 — Comparación de los tres experimentos

**Título:** "El progreso en tres pasos"

**Idea central:** la tabla muestra el progreso acumulado de forma inmediata.

| | Exp. Base | Transfer Learning | Config. Final |
|---|---|---|---|
| Precisión | 51.2% | 70.5% | **91.6%** |
| F1-Score | 0.48 | 0.69 | **0.91** |

**Visual:** tabla con la columna final destacada en naranja o amarillo. Opcionalmente, flechas mostrando +19.3pp y +21.1pp entre columnas.

**Una línea para decir oralmente:** "Cuarenta puntos de mejora en tres experimentos."

---

## SLIDE 26 — Resultados detallados + comparación con la literatura

**Título:** "Un clasificador solo, mejor que dos especializados"

**Parte 1 — Rendimiento balanceado por clase:**

| Clase | Precision | Recall | F1-Score |
|---|---|---|---|
| Técnica Correcta | 0.94 | 0.92 | **0.93** |
| Error de Codos | 0.90 | 0.92 | **0.91** |
| Error de Rodillas | 0.89 | 0.91 | **0.90** |
| **Macro avg** | **0.91** | **0.92** | **0.91** |

El modelo no favoreció ninguna clase — las tres tienen rendimiento similar.

**Parte 2 — Comparación con Parmar et al. (2022):**
- Ellos: dos clasificadores binarios separados. F1 codos = **0.45**, F1 rodillas = **0.84**
- Este trabajo: un único clasificador multiclase. F1 codos = **0.91**, F1 rodillas = **0.90**
- Un solo modelo supera a dos modelos especializados del mismo paper de referencia, sobre el mismo dataset.

**Asset:** `[PLACEHOLDER: assets/resultados/matriz_confusion.png]` — colocar junto a la tabla

---

## SLIDE 27 — Conclusiones

**Título:** "Lo que se logró"

**Formato:** puntos cortos, no párrafos. Uno por objetivo comprometido.

- Pipeline completo: video crudo → evaluación de técnica. Documentado y reproducible.
- 91.6% de precisión, F1-Score macro 0.91 sobre dataset real etiquetado
- Contribución técnica original: algoritmo de corrección de tracking (87% de discontinuidades resueltas)
- Software: $0 — alternativa viable frente a sistemas de $10.000–$100.000
- Base metodológica replicable a otros ejercicios

---

## SLIDE 28 — Trabajo futuro

**Título:** "¿Hacia dónde puede crecer?"

**Formato:** lista visual, no párrafos.

- **Más categorías de error:** trayectoria de la barra, activación del core, posición de los pies
- **Localización temporal:** señalar en qué frames del movimiento ocurre el error
- **Otros ejercicios:** sentadilla, peso muerto, press de banca
- **Feedback con LLMs:** traducir la clasificación en instrucciones correctivas en lenguaje natural
- **Validación con usuarios reales:** entrenadores y practicantes

---

## SLIDE 29 — Cierre personal

**Sin título** (o simplemente "Gracias")

**Contenido:**
- `[PLACEHOLDER: frame/thumbnail del video personal en Corea — assets/personal/video mio en corea mientras investigaba.mp4]`
- Una o dos líneas sobre el recorrido: empezó con conocimientos básicos en IA, llegó a implementar un sistema con resultados publicables, pasando por POSTECH y UCA Cádiz.
- Agradecimientos generales: familia, Agustina, amigos, tutora, intercambios, UCASAL.

**Nota:** este slide es intencionalmente liviano. El trabajo técnico ya fue evaluado — este es el cierre humano.

---

## Resumen estructural

| # | Título | Acción |
|---|---|---|
| 1–10 | Portada → Heurística inicial | Ya finalizados |
| 11 | Meta-instrucción interna | **Eliminar** |
| 12 | Obtención del dataset | Llenar |
| 13 | CV para estimación de poses | Llenar |
| 14 | ViTPose (concepto) | Llenar |
| 15 | ViTPose (implementación + GIF) | Llenar |
| 16 | De ViTPose a PoseConv3D | Llenar |
| 17 | Preprocesamiento: Iteración 1 | Llenar |
| 18 | Preprocesamiento: Iteración 2 | Llenar |
| 19 | Preprocesamiento: Iteración 3 | Llenar |
| 20 | "~60% del trabajo" | No tocar |
| 21 | PoseConv3D (concepto) | **Agregar nueva** |
| 22 | Experimento 1: baseline | **Agregar nueva** |
| 23 | Experimento 2: transfer learning | **Agregar nueva** |
| 24 | Experimento 3: config. final | **Agregar nueva** |
| 25 | Comparación de los 3 experimentos | **Agregar nueva** |
| 26 | Resultados por clase + literatura | **Agregar nueva** |
| 27 | Conclusiones | **Agregar nueva** |
| 28 | Trabajo futuro | **Agregar nueva** |
| 29 | Cierre personal | **Agregar nueva** |

**Total final: 28 slides** (slide 11 eliminada)
