# Slides Brief — Defensa de Tesis
## Ignacio Villanueva | UCASAL 2026

**IMPORTANTE:** La sección "Contenido" de cada slide no es texto literal para copiar en la diapositiva. Es la información que debe estar presente, pero el diseño tiene libertad creativa total para encontrar la forma visual más efectiva de comunicarla. Lo que no cambia son los números, nombres de herramientas y métricas del `data_document.md` — esos sí son exactos y no se inventan.

**Duración estimada:** 25–30 minutos de presentación
**Audiencia:** Tribunal académico de ingeniería. Algunos con background en IA/deep learning, otros no. Todos con criterio técnico general.
**Tono:** Académicamente riguroso pero accesible. Honesto sobre el proceso, incluidos los fracasos intermedios.
**Sistema de diseño:** Opción C — "Narrative Bold" (editorial, cream/dark graphite alternating, naranja #E85D04, tipografía contrastante bold/light)

---

## SLIDE 1 — Portada

**Contenido a comunicar:**
- Título del trabajo
- Nombre del autor y del tutor
- Institución, facultad, carrera y año
- Logo de UCASAL

**Intención:** Primera impresión del tribunal. Seriedad académica con identidad visual moderna. El título es largo — que el diseño lo destaque sin que se sienta apretado. El logo de UCASAL debe estar presente pero no dominar.

**Asset:** `assets/logo-ucasal.png`

---

## SLIDE 2 — El camino de formación

**Contenido a comunicar:**
- Recorrido: UCASAL (Salta, Argentina) → Universidad de Cádiz (España) → POSTECH (Corea del Sur)
- Idea central: los intercambios académicos proveyeron los fundamentos en visión por computadora y aprendizaje profundo que hicieron posible este proyecto

**Intención:** Humanizar la presentación y establecer credibilidad. El jurado necesita saber quién está presentando y por qué tiene autoridad sobre estos temas. La narrativa de "fui a aprender donde esto se hacía de verdad" es poderosa. Puede ser un mapa, una línea de tiempo, íconos de cada institución — lo que transmita el viaje mejor.

---

## SLIDE 3 — El origen del proyecto

**Contenido a comunicar:**
- El punto de partida: una conversación con el Instituto de Rehabilitación de UCASAL planteó la pregunta de si una cámara puede evaluar si alguien ejecuta bien un ejercicio
- Contraste visual: técnica correcta vs. error en el overhead press

**Intención:** Anclar el trabajo en un problema real y local. Evitar que parezca abstracto. El jurado de UCASAL valorará que el origen esté en la propia universidad. Las imágenes del ejercicio correcto vs. incorrecto hacen tangible el problema de forma inmediata.

**Assets:**
- `assets/imagenes_teoricas/01 overhead-press correct technique.jpg`
- `assets/imagenes_teoricas/01 error overhead-press-legs.jpg`

---

## SLIDE 4 — El problema

**Contenido a comunicar:**
- Sin supervisión: riesgo de lesión por mala técnica sin detección
- Con supervisión humana: caro, subjetivo, no escalable
- La evaluación manual depende del ojo y la experiencia del entrenador

**Intención:** Establecer que hay un problema genuino antes de presentar la solución. Breve, visual, directo. Que alguien ajeno al área salga de este slide pensando "sí, eso es un problema real".

---

## SLIDE 5 — Las alternativas existentes y su costo

**Contenido a comunicar (datos exactos del `data_document.md`):**

| Sistema | Tecnología | Costo |
|---|---|---|
| VICON / OptiTrack | Captura de movimiento 3D | USD $10,000–$100,000+ |
| Physimax / Kaia Health | IA para análisis de movimiento | USD $50–$200/mes |
| Tempo / Mirror | Hardware dedicado + software | USD $1,500 + $39/mes |
| **Este proyecto** | **Video RGB estándar + open-source** | **$0** |

**Intención:** Las soluciones existentes son inaccesibles para instituciones educativas o centros de rehabilitación pequeños. El "$0" de la última fila debe impactar visualmente — es el contraste que justifica la existencia del proyecto.

---

## SLIDE 6 — La solución: el pipeline completo

**Contenido a comunicar:**
- Flujo: Video crudo → ViTPose → Keypoints JSON → PoseConv3D → Clasificación (3 clases)
- Las 3 clases de salida: Técnica Correcta / Error de Codos / Error de Rodillas
- Imagen del diagrama de arquitectura

**Intención:** Este es el corazón conceptual de la presentación. El jurado debe salir entendiendo qué hace el sistema aunque no entienda los detalles. Diagrama limpio, flechas claras, mínimo texto. La imagen de arquitectura detallada puede estar como referencia visual de fondo o complemento.

**Asset:** `assets/pipeline/arquitectura detallada.jpg`

---

## SLIDE 7 — ViTPose: estimación de poses

**Contenido a comunicar:**
- Función: detecta 17 puntos articulares en cada frame del video usando Vision Transformers
- Enfoque top-down: YOLOv8 primero detecta personas, ViTPose estima la pose dentro de cada bounding box
- Estándar COCO 17: nariz, ojos, orejas, hombros, codos, muñecas, caderas, rodillas, tobillos
- Ejemplo real: uno de los videos con el esqueleto dibujado sobre la persona

**Intención:** Explicar ViTPose de forma accesible. El jurado técnico apreciará los detalles de Vision Transformers; el jurado general solo necesita ver que "toma el video y dibuja un esqueleto". Los videos con keypoints son la ilustración perfecta.

**Assets:**
- `assets/imagenes_teoricas/2.5 keypoints COCO diagram.png`
- `assets/imagenes_teoricas/2.4 Dosovitskiy ViT architecture.png`
- `videos_keypoints/correct_79235_2_kp.mp4` (o cualquiera de los 6)

---

## SLIDE 8 — PoseConv3D: clasificación temporal

**Contenido a comunicar:**
- Función: analiza la secuencia completa de 48 frames y clasifica en una de 3 categorías
- La diferencia clave con una CNN simple: no analiza fotos aisladas, analiza movimiento completo a lo largo del tiempo
- Dataset de entrenamiento: 2,135 videos etiquetados del Fitness-AQA
- Backbone: ResNet3D SlowOnly, 12 millones de parámetros
- Imagen de convolución 3D (tiempo + espacio)

**Intención:** La distinción "un frame vs. una secuencia" es clave para entender por qué PoseConv3D y no una CNN clásica. Los 48 frames = el sistema ve el movimiento completo, no una foto del momento.

**Asset:** `assets/imagenes_teoricas/2.8 tensorflow 3DCNN.png`

---

## SLIDE 9 — El problema del tracking

**Contenido a comunicar:**
- ViTPose procesa cada frame independientemente — sin memoria entre frames
- Los IDs de personas se reasignan frame a frame
- Ejemplo concreto: en frame 18 la persona tiene ID "44" → desaparece 2 frames por oclusión → reaparece en frame 21 con ID "51" (misma persona, nuevo ID)
- Consecuencia: el modelo recibe lo que parecen ser múltiples personas distintas en lugar de una sola

**Intención:** Este es el problema técnico no obvio que requirió solución original. El jurado debe entender que no era un bug del código sino una limitación arquitectural de ViTPose. Preparar el terreno para el slide 10.

---

## SLIDE 10 — Solución: algoritmo de corrección de tracking

**Contenido a comunicar (datos exactos):**
- Contribución técnica original del proyecto
- La regla: si una persona desaparece ≤3 frames consecutivos Y reaparece a ≤25 píxeles de distancia euclidiana → se mantiene el ID original
- Resultado: 87% de las discontinuidades corregidas en validación
- Secuencias temporales coherentes → modelo con contexto correcto

**Intención:** Momento de orgullo técnico de la presentación. El algoritmo es elegante en su simplicidad y fue desarrollado específicamente para este proyecto. Los números concretos (3 frames, 25px, 87%) dan credibilidad empírica. Un diagrama simple del algoritmo ayuda más que texto.

---

## SLIDE 11 — Proceso iterativo: Experimento Base

**Contenido a comunicar (datos exactos):**
- Configuración: ResNet3D SlowOnly entrenado desde cero, sin weights preentrenados
- Resultado: 51.2% precisión (para referencia: azar en 3 clases = 33.3%)
- F1-Score: 0.48
- Las curvas de pérdida divergen: train baja a ~0.07, validación sube a ~1.5
- Causa: overfitting severo — 12M de parámetros, solo 1,708 videos de entrenamiento

**Intención:** El fracaso inicial es parte honesta del proceso científico. Las curvas divergentes son visualmente contundentes. Este slide establece el baseline que hace que los resultados finales sean impresionantes por contraste.

**Assets:**
- `assets/resultados/baseline_experimento_loss.png`
- `assets/resultados/baseline_experimento_accuracy.png`

---

## SLIDE 12 — Proceso iterativo: Transfer Learning

**Contenido a comunicar (datos exactos):**
- Cambio: inicializar con pesos preentrenados en NTU RGB+D 60 (56,880 videos de movimiento humano)
- Concepto: el modelo ya "sabe" cómo se mueve el cuerpo humano antes de ver overhead press
- Resultado: 70.5% precisión (+19.3 puntos sobre baseline)
- F1-Score: 0.69
- La brecha train/val sigue siendo ~25% — aún hay overfitting, pero menor

**Intención:** Mostrar que el transfer learning fue la palanca más importante, pero no suficiente. Preparar al jurado para entender que el verdadero salto final vino de mejorar los datos, no el modelo.

**Assets:**
- `assets/resultados/experimento_250522_loss.png`
- `assets/resultados/experimento_250522_accuracy.png`

---

## SLIDE 13 — Proceso iterativo: Configuración Final

**Contenido a comunicar (datos exactos):**
- El diferencial clave: reconstrucción del dataset con el algoritmo de tracking corregido
- Cambios adicionales: AdamW (optimizador adaptativo), Pose Jittering (augmentación con ruido Gaussiano σ=2px en coordenadas), label smoothing ε=0.1, CosineAnnealingLR
- Resultado: 91.6% precisión, F1-Score macro 0.91
- Brecha train/val: solo 2–4% — convergencia estable, sin overfitting
- Mejora total: +40.4 puntos sobre el baseline

**Intención:** El mensaje central es que el salto de 70% a 92% no vino de un modelo más complejo sino de datos de mejor calidad. Es una lección de data science que el jurado técnico valorará.

**Assets:**
- `assets/resultados/experimento_250525_loss.png`
- `assets/resultados/experimento_250525_accuracy.png`

---

## SLIDE 14 — Resultados: comparación de experimentos

**Contenido a comunicar (datos exactos):**

| Configuración | Precisión | F1-Score |
|---|---|---|
| Experimento Base | 51.2% | 0.48 |
| Transfer Learning | 70.5% | 0.69 |
| **Configuración Final** | **91.6%** | **0.91** |

**Intención:** Tabla de síntesis limpia. El progreso acumulado debe ser visualmente obvio de inmediato. La fila final debe destacarse con claridad.

---

## SLIDE 15 — Resultados: detalle por clase y comparación con literatura

**Contenido a comunicar (datos exactos):**

Métricas por clase:
| Clase | Precision | Recall | F1-Score |
|---|---|---|---|
| Técnica Correcta | 0.94 | 0.92 | 0.93 |
| Error de Codos | 0.90 | 0.92 | 0.91 |
| Error de Rodillas | 0.89 | 0.91 | 0.90 |
| **Macro avg** | **0.91** | **0.92** | **0.91** |

Comparación referencial con Parmar et al. (2022):
- Ellos: dos clasificadores binarios especializados. F1 codos = 0.45, F1 rodillas = 0.84
- Este trabajo: un único clasificador multiclase. F1 codos = 0.91, F1 rodillas = 0.90

**Intención:** Mostrar que el modelo es balanceado entre clases. La comparación con el trabajo previo es importante — ellos usaron dos clasificadores especializados para el mismo dataset y este trabajo los supera con un único modelo general.

**Asset:** `assets/resultados/matriz_confusion.png`

---

## SLIDE 16 — Conclusiones

**Contenido a comunicar:**
- Los 4 objetivos específicos del trabajo fueron cumplidos (ver objetivos en `data_document.md`)
- Pipeline completo, funcional, documentado y reproducible
- Contribución técnica original: algoritmo de corrección de tracking
- Alternativa accesible frente a sistemas comerciales de $10K–$100K
- Base metodológica replicable para otros ejercicios

**Intención:** Síntesis directa. El jurado evaluará si el trabajo cumplió lo que prometió. Cada punto debe mapear a un objetivo concreto. No sobreexplicar — la defensa es el momento de responder preguntas, no de repetir todo.

---

## SLIDE 17 — Trabajo futuro

**Contenido a comunicar:**
- Más categorías de error: trayectoria de barra, activación del core, posición de los pies
- Localización temporal del error: señalar en qué momento del movimiento ocurre el error
- Expansión a otros ejercicios: sentadilla, peso muerto, press de banca
- Integración con LLMs para feedback correctivo en lenguaje natural
- Validación con usuarios reales: entrenadores y practicantes

**Intención:** Mostrar madurez investigativa. El autor conoce las limitaciones del trabajo y tiene visión de hacia dónde puede crecer. No es un slide de disculpas — es un roadmap de posibilidades.

---

## SLIDE 18 — Cierre personal

**Contenido a comunicar:**
- Imagen o frame del video personal de Corea
- Reflexión sobre el recorrido: empezó con conocimientos básicos en IA, llegó a implementar un sistema con resultados publicables, pasando por dos continentes
- Agradecimientos a la familia, amigos, tutora, equipo de intercambio, UCASAL (sin nombrar personas específicas)

**Intención:** Aterrizaje emocional honesto. El jurado ya evaluó el trabajo técnico — este slide les recuerda que detrás hay una persona que recorrió un camino. No sentimental, sí auténtico. Cierre que deja una impresión humana antes de abrir la ronda de preguntas.

**Asset:** `assets/personal/video mio en corea mientras investigaba.mp4` (usar frame o thumbnail)
