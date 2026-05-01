# DEVLOG - Defensa de Tesis: Materiales de Presentación

## Estado Actual

Proyecto de preparación de materiales para la defensa del PFG de Ignacio Villanueva (UCASAL 2026). La presentación activa es la **v8** (47 slides en Gamma). El usuario construye las slides en tiempo real en Gamma mientras genera conceptos en sesión.

Estado del v8 (2026-04-23):
- Slides 1–31: completas (portada, contexto, dataset, CV básica, YOLO, ViTPose, COCO, implementación, preprocesamiento con 3 iteraciones, slide "60% del trabajo")
- Slide 32: puente "¿cómo entreno una IA?" — existe, correcto
- Slides 33–39: placeholders/vacíos — contenido propuesto en `v8/poseconv3d_puente.md`
- Slide 40: arquitectura final — existe, correcto
- Slide 41: costos $0 — existe, correcto
- Slides 42–43: resultados y discusión — placeholders pendientes
- Slides 44–46: conclusiones, trabajo futuro, cierre — completos
- Slide 47: meta-instrucción interna (eliminar antes de presentar)

El entregable más reciente es **v8/poseconv3d_puente.md** con el contenido literal para las slides 33–39.

## Tareas Activas

- [ ] Aplicar `v8/poseconv3d_puente.md` en Gamma (slides 33–39)
- [ ] Completar slides 42–43 (Resultados y Discusión) — pendiente de sesión futura
- [ ] Insertar assets en slides que los necesiten: GIFs (slide 33), curvas de experimentos (slides 37–39), matriz de confusión (slide 42 o nueva)
- [ ] Eliminar slide 47 (meta-instrucción) antes de la defensa
- [ ] Ensayo cronometrado (objetivo: 25–30 min)

## Decisiones de Arquitectura

- **23 slides, 5 actos**: estructura narrativa que lleva de la pregunta → el sistema → el recorrido experimental → resultados → proyección. Los 4 puentes verbales entre actos no son slides sino frases habladas.
- **v4 como edición sobre v2**: Gamma genera presentaciones muy literales cuando el prompt es muy detallado. La solución fue pasar instrucciones de "qué cambiar" sobre el v2 ya existente.
- **Un clasificador multiclase vs. dos binarios**: el paper de referencia (Parmar et al. 2022) usa 2 clasificadores binarios. Este trabajo usa 1 multiclase y supera ambos. Esto es un punto narrativo clave en S18.
- **El algoritmo de corrección de tracking como contribución técnica original**: el problema de IDs fragmentados por ViTPose no estaba documentado. El algoritmo (≤3 frames de ausencia + ≤25 px de distancia) corrigió 87% de discontinuidades y fue determinante para pasar de 70.5% → 91.6%.

## Sesiones

### 2026-04-23 - Sesión 3
**Objetivo:** Proponer contenido del bloque PoseConv3D + experimentos (slides 33–39 del v8)
**Hecho:**
- Lectura completa del v8 (47 slides) para mapear estado actual
- Generado `v8/poseconv3d_puente.md` con contenido literal para 7 slides (33–39)
- Sesión conceptual extensa: CNN, YOLO, Transformers, ViTPose — el usuario construyó slides de CV en tiempo real
**Decisiones:**
- Slide 33: "Una foto no alcanza" — el GIF de técnica correcta como imagen visual; los bullets plantean el problema del análisis por frame
- Slide 34: "De 2D a 3D" — con la imagen de 3DCNN como único elemento visual; no explicar qué es entrenar (ya implícito por la progresión)
- Slide 35: PoseConv3D — tabla comparativa vs. alternativas (CNN 2D / LSTM / PoseConv3D) para justificar la elección sin vender humo
- Slides 36–39: resumen de 3 experimentos + slides individuales; los títulos llevan el porcentaje de resultado para que el progreso sea visible de un vistazo
- La slide 36 funciona como "mapa" antes de los 3 experimentos — equivalente a la slide de agenda
**Próximos pasos:**
- Aplicar `v8/poseconv3d_puente.md` en Gamma
- Completar slides 42–43 (Resultados y Discusión)
- Insertar assets en slides que los necesiten
- Ensayo cronometrado

### 2026-04-23 - Sesión 2
**Objetivo:** Definir contenido para los placeholders del v5 (slides 12–19) y las slides faltantes (21–29)
**Hecho:**
- Lectura completa del PDF de la tesis (todos los capítulos relevantes)
- Generado `v6_slides_recomendaciones.md` con recomendaciones detalladas slide por slide
- Estructura final: 28 slides (slide 11 eliminada, 9 slides nuevas agregadas después de slide 20)
**Decisiones:**
- Slide 16 introduce el problema de tracking como "gancho" antes de las iteraciones 17–19
- Slide 21 (PoseConv3D) se agrega después del "~60% del trabajo" para cerrar el bloque de arquitectura antes de los experimentos
- Los 3 experimentos llevan en el título su resultado-clave (51.2% / 70.5% / 91.6%) para que el progreso sea visible de un vistazo
- Cada experimento detalla los cambios aplicados y qué significan — no solo los números
**Próximos pasos:**
- Aplicar el v6_slides_recomendaciones.md en Gamma
- Insertar assets (GIFs, curvas, matriz confusión)
- Ensayo cronometrado

### 2026-04-22 - Sesión 1
**Objetivo:** Analizar el v2 y producir materiales de rediseño completos  
**Hecho:**
- Diagnóstico del v2 (5 problemas: múltiples ideas por slide, texto denso, errores de producción, sin demo, narrativa experimental sepultada)
- Propuesta de estructura en 5 actos con 23 slides
- v3/slides-gamma.md: prompt completo listo para pegar en Gamma en 2 lotes
- v3/guion.md: speech slide por slide (~18-19 min, primera persona)
- v3/info-extra.md: sistema de estilos, cronograma, placeholders de assets, checklist
- v4/cambios-sobre-v2.md: instrucciones de edición sobre el v2 existente
- v4/guion.md: guion ajustado a la estructura v4  
**Decisiones:**
- v4 en lugar de v3 porque Gamma es demasiado literal con prompts detallados
- Insertar S6 "Objetivos y alcance" después de justificar el problema  
**Proximos pasos:**
- Usuario aplica cambios en Gamma
- Asignar GIFs a placeholders
- Ensayo cronometrado
