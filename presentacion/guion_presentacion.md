# Guión de Presentación — Defensa de Tesis
## Apoyo para el speech oral — no va en Canva

Este documento no es un script palabra por palabra. Es una referencia para preparar lo que decís mientras el slide está en pantalla. El slide orienta; vos explicás.

---

## GLOSARIO DE TÉRMINOS TÉCNICOS
*Cómo explicar cada concepto en pocas palabras, sin perder precisión*

---

### "Entrenar desde cero"
**Qué significa:** el modelo empieza sin ningún conocimiento previo sobre el mundo. Sus 12 millones de parámetros están inicializados con valores aleatorios — básicamente, no sabe nada. Para aprender a distinguir técnica correcta de errores, tiene que extraer esos patrones únicamente de los 1,708 videos de entrenamiento.

**Cómo explicarlo en la defensa:**
> "Entrenar desde cero significa que el modelo parte de cero conocimiento. Es como pedirle a alguien que nunca vio movimiento humano que aprenda a detectar errores en un ejercicio, viendo solo 1,700 ejemplos. Con 12 millones de parámetros para ajustar, inevitablemente termina memorizando esos ejemplos en lugar de aprender patrones generalizables."

**Señal de que salió mal:** la curva de pérdida de entrenamiento baja (el modelo "aprende"), pero la de validación sube (no generaliza). Eso es overfitting.

---

### Transfer Learning
**Qué significa:** en lugar de empezar desde cero, usamos un modelo que ya fue entrenado en 56,880 videos de movimiento humano (dataset NTU60 — personas caminando, aplaudiendo, levantando objetos). Ese modelo ya "sabe" cómo se mueven los cuerpos. Nosotros lo tomamos y lo ajustamos para que aprenda a distinguir overhead press correcto de incorrecto.

**Cómo explicarlo en la defensa:**
> "El transfer learning es como contratar a alguien que ya tiene experiencia analizando movimiento humano, en lugar de enseñarle todo desde cero. El modelo ya vio 56,000 videos de personas moviéndose — no exactamente el ejercicio que nos importa, pero sí el lenguaje base del movimiento. Con esa base, 1,700 ejemplos específicos son suficientes para especializarse."

**Resultado:** +19 puntos porcentuales sobre el baseline. El conocimiento previo importa.

---

### Overfitting
**Qué significa:** el modelo "memoriza" los ejemplos de entrenamiento en lugar de aprender patrones generalizables. Funciona perfecto con datos que ya vio, pero falla con datos nuevos.

**Cómo explicarlo en la defensa:**
> "El overfitting es cuando el modelo se vuelve demasiado específico. Aprende de memoria 'este video particular tiene error de codos' en lugar de aprender 'los codos que se abren así generalmente indican error'. Cuando le mostrás un video nuevo, no reconoce el patrón."

**Señal visual:** las dos curvas (entrenamiento y validación) divergen. La de entrenamiento baja sola; la de validación sube o se estanca.

---

### AdamW (optimizador)
**Qué significa:** es el algoritmo que actualiza los pesos del modelo durante el entrenamiento. SGD (el anterior) aplicaba la misma tasa de actualización a todos los parámetros. AdamW calibra cuánto actualizar cada parámetro según su historial individual — parámetros que cambiaron mucho antes se actualizan más despacio; parámetros más estables se pueden ajustar más.

**Cómo explicarlo en la defensa:**
> "El cambio de SGD a AdamW es como pasar de regar todas las plantas con el mismo caudal a darle a cada una la cantidad que necesita según cómo está. Es un optimizador más inteligente — ajusta la intensidad de cada ajuste según el comportamiento previo de ese parámetro. En redes profundas complejas, eso hace diferencia."

**Número concreto:** bajamos el learning rate de 0.05 (SGD) a 0.001 (AdamW) — 20 veces menor, pero más preciso.

---

### Pose Jittering
**Qué significa:** durante el entrenamiento, se agrega ruido aleatorio pequeño (desviación estándar de 2 píxeles) a las coordenadas de los keypoints. Si el codo está en el punto (230, 145), en algunos ejemplos de entrenamiento aparece en (231, 143) o (229, 147).

**Por qué:** ViTPose no es perfectamente preciso — su localización de articulaciones varía ligeramente frame a frame. Si el modelo aprende con coordenadas exactas, se vuelve frágil ante esa imprecisión natural.

**Cómo explicarlo en la defensa:**
> "Pose Jittering es una técnica de aumento de datos. Durante el entrenamiento, movemos levemente los puntos articulares de forma aleatoria — unos pocos píxeles. Así el modelo aprende que una rodilla en (230, 145) y en (232, 143) son la misma rodilla en la misma posición. Lo hace robusto a la imprecisión natural del detector de pose."

---

### Label Smoothing
**Qué significa:** en lugar de decirle al modelo "este video es 100% error de codos", le decimos "es 90% error de codos, 5% técnica correcta, 5% error de rodillas" (ε=0.1). Se suaviza la etiqueta.

**Por qué:** si el modelo aprende que siempre tiene que predecir con 100% de confianza, se vuelve excesivamente seguro de sí mismo. Eso lo hace más frágil ante casos ambiguos.

**Cómo explicarlo en la defensa:**
> "Label smoothing le dice al modelo que sea un poco menos categórico. En lugar de exigirle certeza absoluta, le pedimos que distribuya un pequeño porcentaje de probabilidad entre las otras clases. Eso lo hace más calibrado — cuando hay ambigüedad real, no predice con falsa confianza."

---

### Heatmap de keypoints
**Qué significa:** en lugar de guardar la posición de cada articulación como un par de coordenadas (x, y), se genera una imagen pequeña (56×56 píxeles) para cada articulación donde el punto brillante representa dónde está la articulación. 17 articulaciones × 48 frames = el volumen espacio-temporal que procesa PoseConv3D.

**Cómo explicarlo en la defensa:**
> "PoseConv3D no trabaja con coordenadas numéricas sino con mapas de calor — pequeñas imágenes donde el punto brillante marca dónde está cada articulación. Eso permite aplicar las mismas convoluciones que funcionan en video a las secuencias de esqueletos."

---

## QUÉ DECIR EN CADA SLIDE CLAVE

---

### Slide 7 — ¿Por qué ViTPose?

**Apertura sugerida:**
> "Para detectar las articulaciones en cada frame, elegí ViTPose. ¿Por qué esta herramienta y no otras como OpenPose o MediaPipe?"

**Desarrollo oral:**
> "Las herramientas tradicionales de estimación de pose analizan la imagen en partes pequeñas. Para saber si el codo está bien posicionado, tienen que juntar información de muchos parches distintos de la imagen — eso puede generar errores cuando las articulaciones están cerca unas de otras o se tapan. ViTPose, basado en Vision Transformers, ve todas las articulaciones en relación desde el primer momento. Es como la diferencia entre mirar el cuerpo parte por parte versus verlo todo de un vistazo — la segunda forma da mucho más contexto."

---

### Slide 12 — La lógica de los experimentos

**Apertura sugerida:**
> "Antes de mostrar los números, quiero explicar la lógica detrás de los tres experimentos. Cada uno fue una pregunta."

**Desarrollo oral:**
> "El primer experimento preguntó: ¿puede el modelo aprender este problema desde cero? La respuesta fue no — con 12 millones de parámetros y solo 1,700 videos, memoriza en lugar de aprender. El segundo preguntó: ¿ayuda darle conocimiento previo? Sí, saltamos casi 20 puntos. Pero todavía había una brecha grande entre entrenamiento y validación. El tercero preguntó: ¿el problema era el modelo o los datos? Los datos. Cuando corregimos el tracking y mejoramos la calidad de los datos, el modelo convergió."

---

### Slide 15 — Qué cambia y por qué

**Apertura sugerida:**
> "La configuración final involucró cuatro cambios respecto al experimento anterior. No los hice al azar — cada uno atacó un problema específico."

**Desarrollo oral:**
> "El más importante fue reconstruir el dataset con el tracking corregido. El modelo estaba viendo hasta diez 'personas distintas' en un video donde había una sola. Eso hacía incoherentes las secuencias temporales — no podía aprender el movimiento de un sujeto porque lo veía fragmentado. Los otros tres cambios — AdamW, Pose Jittering, Label Smoothing — mejoraron la regularización para que el modelo no se sobreajustara a los datos de entrenamiento."

---

### Slide 18 — La comparación académica

**Apertura sugerida:**
> "El trabajo más cercano al nuestro en la literatura es Parmar et al. de 2022, que usó el mismo dataset."

**Desarrollo oral:**
> "La diferencia clave de estrategia: ellos entrenaron dos clasificadores separados, uno para detectar errores de codos y otro para errores de rodillas. Cada uno es binario — sí o no. Yo entrené un único clasificador que distingue las tres clases simultáneamente. El resultado: en codos, mi F1 es 0.91 contra su 0.45 — más del doble. En rodillas, 0.90 contra 0.84. Y noten la inconsistencia en sus resultados: 0.45 en codos y 0.84 en rodillas. Esa disparidad sugiere inestabilidad entre clasificadores. Un modelo unificado captura mejor las relaciones entre los distintos tipos de error."

---

### Slide 20 — Qué dice la matriz de confusión

**Apertura sugerida:**
> "Esta es la matriz de confusión del modelo final. Déjenme leerla."

**Desarrollo oral:**
> "La diagonal — los números más grandes — son los aciertos: los videos que el modelo clasificó correctamente en cada clase. Los números fuera de la diagonal son los errores. Lo que me interesa destacar es que los errores cruzados entre las dos clases de error son muy bajos — el modelo distingue bien error de codos de error de rodillas, que son los casos más difíciles de separar. Y las tres clases tienen F1 prácticamente igual: 0.93, 0.91 y 0.90. Eso indica que el modelo no se sesgó hacia la clase con más ejemplos — aprendió características discriminativas reales."

---

## PREGUNTAS ESPERADAS DEL JURADO

---

**"¿Por qué eligieron el overhead press y no otro ejercicio?"**
> "Por dos razones. Primero, el Instituto de Rehabilitación de UCASAL identificó este ejercicio como un caso de uso concreto. Segundo, existe trabajo previo en el mismo ejercicio con el mismo dataset (Parmar et al. 2022), lo que me permite hacer una comparación directa y válida. No podría comparar contra el estado del arte si hubiera elegido un ejercicio sin benchmark establecido."

---

**"¿Por qué no validaron con usuarios reales?"**
> "Es una limitación explícita del trabajo. La validación se hizo sobre el dataset académico Fitness-AQA. La validación con usuarios reales — comparar la clasificación del sistema contra la evaluación de entrenadores expertos — es el primer paso natural del trabajo futuro. Sería el paso de laboratorio a campo."

---

**"¿Cuánto tarda en procesar un video?"**
> "Menos de 2 segundos por video en GPU. El cuello de botella es la extracción de keypoints con ViTPose, no la clasificación. No corre en tiempo real — requiere el video completo — pero es lo suficientemente rápido para uso práctico."

---

**"¿Por qué ViTPose y no MediaPipe, que es gratuito y más liviano?"**
> "MediaPipe es una buena opción para aplicaciones en tiempo real con recursos limitados. Para este trabajo, la precisión de detección de pose importaba más que la velocidad — un keypoint mal detectado en frames críticos del movimiento puede cambiar la clasificación. ViTPose tiene mejor desempeño en benchmarks estándar de estimación de pose, especialmente en poses complejas donde las articulaciones se tapan entre sí — lo cual es común en el overhead press."

---

**"¿Qué pasa si el video tiene más de una persona?"**
> "El pipeline detecta a la persona con el bounding box más grande en el primer frame y la sigue durante todo el video. En el contexto del dataset — videos de un solo atleta haciendo el ejercicio — esto es suficiente. Para escenarios con múltiples personas simultáneas, el algoritmo de tracking requeriría adaptaciones adicionales."

---

**"¿Podrían usar el sistema sin GPU?"**
> "La extracción de keypoints con ViTPose es computacionalmente costosa y funciona mejor con GPU. La clasificación con PoseConv3D sobre los keypoints ya extraídos es más liviana. En la práctica, el cuello de botella es la fase de estimación de pose. Una posible arquitectura de producción sería procesar los videos en la nube y devolver la clasificación al usuario."

---

**"¿Por qué 48 frames y no más o menos?"**
> "48 frames es la configuración del paper original de PoseConv3D y del dataset Fitness-AQA. Representa un balance entre capturar el movimiento completo del ejercicio — que dura típicamente 2 a 5 segundos — y mantener el costo computacional manejable. Los frames se muestrean uniformemente del video completo, independientemente de su duración original."

---

*Este documento evoluciona. A medida que practiques la presentación, añadí las preguntas que surjan y las respuestas que funcionen mejor.*
