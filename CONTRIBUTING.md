# Guía de contribución — QuantRoute

¡Gracias por tu interés en contribuir a QuantRoute! Este documento te guía en el proceso.

## Código de conducta

Este proyecto sigue el principio de colaboración abierta y respetuosa. Toda interacción debe ser profesional y constructiva.

## ¿Cómo contribuir?

### Reportar bugs

Si encuentras un bug, abre un **Issue** con:
- Descripción clara del problema
- Pasos para reproducirlo
- Comportamiento esperado vs. observado
- Versión de Python y sistema operativo

### Proponer mejoras

Abre un **Issue** etiquetado como `enhancement` con:
- Descripción del problema que resuelve
- Propuesta de implementación
- Impacto esperado en rendimiento o usabilidad

### Pull Requests

1. Haz fork del repositorio
2. Crea una rama descriptiva:
   ```bash
   git checkout -b feature/vrptw-time-windows
   git checkout -b fix/aco-pheromone-evaporation
   git checkout -b docs/api-examples
   ```
3. Escribe código limpio y documentado
4. Asegúrate de que el código existente sigue funcionando
5. Abre el PR con descripción detallada

## Estándares de código

### Python (backend)

```python
# Usar type hints siempre
def tour_cost(tour: List[int], D: np.ndarray) -> float:
    """
    Calcula el costo total de un tour.
    
    Args:
        tour: Lista de índices de nodos en orden de visita
        D: Matriz de distancias NxN
    
    Returns:
        Suma de distancias euclidianas del tour completo
    """
    return sum(D[tour[i]][tour[(i + 1) % len(tour)]] for i in range(len(tour)))
```

- Docstrings en todas las funciones públicas
- Type hints en parámetros y retornos
- Nombres en inglés, comentarios pueden ser en español
- Máximo 100 caracteres por línea

### JavaScript (frontend)

- Comentarios explicativos en secciones complejas
- Variables con nombres descriptivos
- Separar lógica de algoritmo de lógica de render

## Áreas prioritarias

| Área | Dificultad | Impacto |
|------|-----------|---------|
| Implementar VRPTW (time windows) | Alta | Alto |
| Integrar Google Maps API | Media | Alto |
| Tests unitarios para algoritmos | Media | Alto |
| Docker Compose setup | Baja | Medio |
| Exportar rutas a GeoJSON/GPX | Baja | Medio |
| Algoritmo QUBO para D-Wave | Muy Alta | Alto |

## Contacto

**Skila — Strategic Knowledge & Learning Academy**  
GitHub: [@skila-academy](https://github.com/skila-academy)
