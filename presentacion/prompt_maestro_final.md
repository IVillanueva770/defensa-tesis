# Prompt Maestro — Defensa de Tesis
## Para usar en Claude Design / Canva AI / Herramienta de generación de slides

---

## CONTEXTO DEL PROYECTO

Necesito una presentación de defensa de tesis universitaria de 18 slides para 25–30 minutos. El trabajo se llama "Evaluación Automatizada de Técnica en Ejercicios de Fitness mediante Aprendizaje Profundo y Visión por Computadora". Lo presentaré ante un tribunal académico de ingeniería en UCASAL (Argentina). Es mi Proyecto Final de Grado.

El sistema que desarrollé analiza videos de personas haciendo overhead press (press de barra sobre la cabeza) y clasifica automáticamente si la técnica es correcta o si tiene errores específicos — usando ViTPose para detectar los puntos articulares del cuerpo y PoseConv3D para clasificar el movimiento completo. Logré 91.6% de precisión con F1-macro de 0.91.

**El output debe ser editable** (PPTX, Canva, etc).

---

## SISTEMA DE DISEÑO

### Identidad visual: "Narrative Bold"
Una estética editorial moderna que contrasta slides de fondo oscuro (grafito profundo #1C1C1E) con slides de fondo claro (crema #F5F0E8), alternando para crear ritmo visual. La energía es más de revista de diseño de alta calidad que de presentación corporativa.

### Paleta de colores
- **Fondo oscuro (principal):** #1C1C1E (grafito)
- **Fondo claro (alternado):** #F5F0E8 (crema)
- **Acento primario:** #E85D04 (naranja quemado) — solo para destacar datos clave, números impactantes, headlines de énfasis
- **Texto sobre oscuro:** #F5F0E8 (crema) o blanco #FFFFFF
- **Texto sobre claro:** #1C1C1E (grafito)
- **Secundario neutro:** #8A8A8A (para labels, captions, texto de soporte)

### Tipografía
- **Headlines grandes:** tipografía serif bold (ej. Playfair Display Bold, Georgia Bold) — transmite peso académico
- **Cuerpo y datos:** tipografía sans-serif regular (ej. Inter, DM Sans) — legibilidad y modernidad
- **Números destacados:** misma sans-serif pero en tamaño grande, peso bold — que los números "impacten" visualmente, estén remarcados
- Tamaño mínimo cuerpo: 14pt. Headlines: 24pt mínimo.

### Estilo de layout
- Asimétrico y editorial: no todo centrado, jugar con alineaciones a la izquierda, texto grande con imagen a la derecha, o viceversa
- Mucho espacio blanco (o espacio oscuro) — no llenar todo con texto pero que se entienda bien cuál es el foco, lo importante de cada slide
- Márgenes amplios: al menos 0.75" en todos los lados
- Máximo 5 bullets por slide, preferir menos
- Los slides de datos (tablas, métricas) pueden usar fondo oscuro con los números en naranja o crema grande
- Los slides de imágenes pueden dejar que la imagen respire

### Elementos gráficos
- Líneas finas como separadores o acentos (no bordes gruesos)
- Puede usar formas geométricas simples como marcos o resaltadores
- Evitar iconos genéricos corporativos
- Preferir que las imágenes tengan tratamiento consistente (mismo estilo de recorte, mismos márgenes). Importante que se vean completas.

---

## ESTRUCTURA: 18 SLIDES

### 1. PORTADA
- Título: "Evaluación Automatizada de Técnica en Ejercicios de Fitness mediante Aprendizaje Profundo y Visión por Computadora"
- Autor: Ignacio Villanueva | Tutor: Mg. Lic. Lorena Talamé
- UCASAL — Facultad de Ingeniería e Informática — Ingeniería en Informática | 2026
- Logo UCASAL (archivo: `assets/logo-ucasal.png`)
- Fondo oscuro. El título es largo — tratarlo como pieza editorial, que ocupe espacio con dignidad.

### 2. EL CAMINO DE FORMACIÓN
- Recorrido geográfico del autor: UCASAL (Salta, Argentina) → Universidad de Cádiz (España) → POSTECH (Corea del Sur)
- Idea: los intercambios proveyeron los fundamentos que hicieron posible el proyecto
- Diseño libre: mapa, línea de tiempo, íconos. Que transmita el viaje.

### 3. EL ORIGEN DEL PROYECTO
- Punto de partida: conversación con el Instituto de Rehabilitación de UCASAL → pregunta: ¿puede una cámara evaluar si alguien hace bien un ejercicio?
- Mostrar las dos imágenes lado a lado: técnica correcta vs. error de piernas
- Assets: `assets/imagenes_teoricas/01 overhead-press correct technique.jpg` y `assets/imagenes_teoricas/01 error overhead-press-legs.jpg`

### 4. EL PROBLEMA
- Sin supervisión: riesgo de lesión silencioso
- Con supervisión humana: cara, subjetiva, no escalable
- Breve y directo — 3 ideas máximo

### 5. LAS ALTERNATIVAS EXISTENTES
- Tabla de comparación de costos — la fila del proyecto con "$0" debe resaltar visualmente con naranja o tamaño grande

| Sistema | Tecnología | Costo aproximado |
|---|---|---|
| VICON / OptiTrack | Captura de movimiento 3D con marcadores | USD $10,000–$100,000+ |
| Physimax / Kaia Health | IA para análisis de movimiento, SaaS | USD $50–$200/mes |
| Tempo / Mirror | Hardware dedicado + suscripción software | USD $1,500 + $39/mes |
| **Este proyecto** | **Video RGB estándar + herramientas open-source** | **$0** |

### 6. LA SOLUCIÓN: EL PIPELINE
- Diagrama de flujo: Video → ViTPose → Keypoints JSON → PoseConv3D → 3 clases de salida
- Las 3 clases: Técnica Correcta / Error de Codos / Error de Rodillas
- Asset de referencia: `assets/pipeline/arquitectura detallada.jpg`
- Slide de concepto — que el flujo sea claro aunque no se entiendan los nombres técnicos

### 7. VITPOSE: ESTIMACIÓN DE POSES
- Función: detecta 17 puntos articulares por frame usando Vision Transformers
- Enfoque top-down: YOLOv8 detecta personas → ViTPose estima la pose dentro de cada bounding box
- Mostrar el diagrama de keypoints COCO y/o la arquitectura ViT
- Si es posible embeber o mostrar frame del video con esqueleto: `videos_keypoints/correct_79235_2_kp.mp4`
- Assets: `assets/imagenes_teoricas/2.5 keypoints COCO diagram.png`, `assets/imagenes_teoricas/2.4 Dosovitskiy ViT architecture.png`

### 8. POSECONV3D: CLASIFICACIÓN TEMPORAL
- Función: analiza 48 frames de heatmaps de keypoints y clasifica el movimiento
- Diferencia clave: no una foto, una secuencia de movimiento
- Dataset: 2,135 videos etiquetados del Fitness-AQA (1,708 entrenamiento / 427 validación)
- Backbone: ResNet3D SlowOnly, 12 millones de parámetros
- Asset: `assets/imagenes_teoricas/2.8 tensorflow 3DCNN.png`

### 9. EL PROBLEMA DEL TRACKING
- ViTPose no tiene memoria entre frames — los IDs se reasignan
- Ejemplo visual: persona con ID "44" desaparece → reaparece como ID "51"
- Consecuencia: el modelo ve múltiples personas donde hay una sola
- Este slide prepara al jurado para entender por qué la solución del siguiente slide importa

### 10. ALGORITMO DE CORRECCIÓN DE TRACKING
- Contribución técnica original
- La regla exacta: desaparición ≤3 frames + reaparición ≤25 píxeles → ID original se mantiene
- Resultado: 87% de discontinuidades corregidas
- Puede ser un diagrama visual simple del algoritmo
- No cambiar los números: 3 frames, 25px, 87%

### 11. EXPERIMENTO BASE
- Sin transfer learning. ResNet3D desde cero.
- Precisión: 51.2% (azar = 33.3%). F1: 0.48
- Curvas divergentes: pérdida train ~0.07, pérdida validación ~1.5
- Causa: overfitting — 12M parámetros, solo 1,708 videos
- Assets: `assets/resultados/baseline_experimento_loss.png` y `assets/resultados/baseline_experimento_accuracy.png`

### 12. TRANSFER LEARNING
- Cambio: pesos de NTU60 (56,880 videos de movimiento humano)
- Precisión: 70.5% (+19.3pp sobre baseline). F1: 0.69
- Brecha train/val: ~25% — overfitting reducido pero presente
- Assets: `assets/resultados/experimento_250522_loss.png` y `assets/resultados/experimento_250522_accuracy.png`

### 13. CONFIGURACIÓN FINAL
- La clave: dataset reconstruido con tracking corregido + AdamW + Pose Jittering
- Precisión: 91.6%. F1-macro: 0.91
- Brecha train/val: 2–4% (convergencia estable)
- El salto de 70% → 92% vino de mejores datos, no de un modelo más complejo
- Assets: `assets/resultados/experimento_250525_loss.png` y `assets/resultados/experimento_250525_accuracy.png`

### 14. COMPARACIÓN DE EXPERIMENTOS
- Tabla de tres filas — la fila Final debe destacarse claramente

| Experimento | Precisión (val) | F1-macro |
|---|---|---|
| Baseline (sin transfer learning) | 51.2% | 0.48 |
| Transfer Learning (NTU60) | 70.5% | 0.69 |
| **Configuración Final** | **91.6%** | **0.91** |

### 15. RESULTADOS POR CLASE
- Tabla de métricas por clase:

| Clase | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Técnica Correcta | 0.94 | 0.92 | 0.93 | ~179 |
| Error de Codos | 0.90 | 0.92 | 0.91 | ~128 |
| Error de Rodillas | 0.89 | 0.91 | 0.90 | ~120 |
| **Macro avg** | **0.91** | **0.92** | **0.91** | **427** |

- Matriz de confusión: `assets/resultados/matriz_confusion.png`
- Comparación con Parmar et al. (2022): ellos usaron clasificadores binarios sobre el mismo dataset — F1 codos: 0.45, F1 rodillas: 0.84. Este trabajo logra F1 0.91 global con un clasificador multiclase único.

### 16. CONCLUSIONES
- 4 objetivos específicos: todos cumplidos
- Pipeline completo, documentado y reproducible
- Contribución original: algoritmo de tracking
- Alternativa de $0 frente a sistemas de $10K–$100K+
- Slide de síntesis — conciso, que se lea en 30 segundos

### 17. TRABAJO FUTURO
- Más errores, localización temporal, más ejercicios, integración con LLMs, validación con usuarios reales
- Slide de roadmap — forward-looking, no disculpas

### 18. CIERRE PERSONAL
- Frame o imagen del video: `assets/personal/video mio en corea mientras investigaba.mp4`
- Reflexión sobre el recorrido: de conocimientos básicos en IA a resultados publicables, pasando por dos continentes
- Agradecimientos a familia, amigos, tutora, equipo de intercambio, UCASAL (sin nombres propios)
- Slide emocional honesto — que el diseño lo apoye sin sentimentalismo excesivo

---

## INSTRUCCIONES FINALES PARA EL DISEÑO

1. **Todos los números, porcentajes y métricas son exactos** — no redondear ni parafrasear. Las tablas embebidas en cada slide son la fuente de verdad.

2. **Los slides de contenido no son transcripciones** — el texto de cada slide es una guía de intención. El diseño tiene libertad creativa para encontrar la mejor forma visual de comunicar cada idea.

3. **Alternancia fondo oscuro/claro** — no todos los slides del mismo color. El ritmo visual de alternancia es parte de la identidad.

4. **Slides de datos** (tablas, métricas, gráficos) — fondo oscuro con números grandes y acento naranja funcionan mejor para impacto.

5. **Assets provistos** — respetar los archivos indicados en cada slide. No usar imágenes genéricas cuando hay un asset específico disponible.

6. **Output editable** — el resultado debe poder editarse en Canva o exportarse como PPTX editable. No entregar solo HTML.

7. **Relación de aspecto:** 16:9 estándar.

8. **Tono sobrio** — es una exposición del trabajo realizado, no una presentación de ventas. Títulos confiados pero sin grandilocuencia.

---

## REFERENCIA DE ASSETS

```
assets/
├── logo-ucasal.png                                    → Slide 1
├── imagenes_teoricas/
│   ├── 01 overhead-press correct technique.jpg        → Slide 3
│   ├── 01 error overhead-press-legs.jpg               → Slide 3
│   ├── 2.4 Dosovitskiy ViT architecture.png           → Slide 7
│   ├── 2.5 keypoints COCO diagram.png                 → Slide 7
│   └── 2.8 tensorflow 3DCNN.png                       → Slide 8
├── pipeline/
│   └── arquitectura detallada.jpg                     → Slide 6
├── resultados/
│   ├── baseline_experimento_loss.png                  → Slide 11
│   ├── baseline_experimento_accuracy.png              → Slide 11
│   ├── experimento_250522_loss.png                    → Slide 12
│   ├── experimento_250522_accuracy.png                → Slide 12
│   ├── experimento_250525_loss.png                    → Slide 13
│   ├── experimento_250525_accuracy.png                → Slide 13
│   └── matriz_confusion.png                           → Slide 15
└── personal/
    └── video mio en corea mientras investigaba.mp4    → Slide 18

videos_keypoints/
├── correct_79235_2_kp.mp4                            → Slide 7 (ejemplo técnica correcta)
├── elbows_error_62866_3_kp.mp4                       → Referencia error de codos
└── knees_error_62908_1_kp.mp4                        → Referencia error de rodillas
```
