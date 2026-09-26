# Optimización de Navegación - Sistema STAP (IPS Medialfa)

**Curso:** Arquitectura de Software
**Autor:** Reinmy Aomen Paz Zambrano
**Actividad:** Navegando Mareas (Unidad 3)

## Descripción del Problema (El Cuello de Botella)
El sistema STAP original implementaba un procesamiento del lado del cliente (*Client-Side Processing*). Al consultar el módulo de Historias Clínicas, el ORM de Django extraía más de 2,000 registros históricos de Microsoft SQL Server y los enviaba en un solo bloque JSON. Esto saturaba la memoria RAM del navegador del usuario final, congelaba la interfaz gráfica de DataTables y generaba tiempos de respuesta (latencia) inaceptables.

## Solución Arquitectónica (Procesamiento Server-Side)
Para optimizar el rendimiento y la escalabilidad de la navegación, se migró la responsabilidad de procesamiento hacia el backend, extrayendo de la base de datos únicamente los fragmentos exactos que el usuario está visualizando.

Para ello, se implementaron los siguientes patrones de diseño (ver archivo `views_optimizacion_historias.py`):

*   **Patrón Strategy (Estrategia):** Se diseñó la clase `FiltroHistoriasInteligente` para aislar los algoritmos de filtrado. Esto permite realizar búsquedas dinámicas combinadas directamente en SQL Server (por cédula, nombres, sede o estudio) sin alterar la lógica del controlador principal.
*   **Patrón Iterator (Iterador):** Se implementó la clase `IteradorHistorias` acoplada al paginador de Django. En lugar de extraer miles de registros, el iterador lee los parámetros de navegación de la tabla (`start` y `length`) y ejecuta comandos `OFFSET/FETCH` en SQL Server, retornando bloques ligeros y secuenciales de 10 a 50 registros.

## Resultados de la Optimización
La refactorización arquitectónica redujo el tiempo de renderizado de la tabla de varios segundos a **milisegundos**. Esto liberó por completo la carga computacional del equipo del cliente y protegió la memoria del servidor principal, asegurando una alta disponibilidad del sistema independientemente del crecimiento continuo de la base de datos.

---
*Nota: Por estrictas políticas de seguridad y privacidad de datos médicos de la IPS Medialfa, este repositorio no contiene el sistema monolítico completo. Contiene exclusivamente los módulos (`views_optimizacion_historias.py`, `urls_snippet.py` y `Historias.html`) que evidencian la refactorización y la solución arquitectónica solicitada para la optimización de la navegación.*
