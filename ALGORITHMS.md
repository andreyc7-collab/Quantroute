# Documentación técnica — Algoritmos Quantum-Inspired

> Referencia matemática y de implementación de los tres algoritmos de QuantRoute.

---

## Fundamento teórico: ¿Por qué "quantum-inspired"?

La computación cuántica ofrece ventajas teóricas para problemas de optimización combinatoria. Sin embargo, el hardware cuántico actual (NISQ era) tiene limitaciones de escala y ruido que impiden su aplicación directa a problemas logísticos reales.

Los algoritmos **quantum-inspired** toman los *principios físicos* que hacen poderosa a la computación cuántica —superposición, tunneling, interferencia— y los emulan en hardware clásico mediante heurísticas probabilísticas. El resultado son algoritmos que:

1. Escapan de óptimos locales de forma sistemática (tunneling)
2. Exploran múltiples soluciones en paralelo (superposición)
3. Refuerzan caminos prometedores (amplificación de amplitudes)

---

## Problema base: TSP y sus variantes

### Travelling Salesman Problem (TSP)

**Definición formal:**
- Dado un grafo completo `G = (V, E)` con `n` nodos y pesos `w(i,j)`
- Encontrar la permutación `π` de `V` que minimiza:

```
min Σ w(π(i), π(i+1))   para i = 1..n, con π(n+1) = π(1)
i=1
```

**Complejidad:** NP-hard. El número de rutas posibles es `(n-1)!/2`.

| n nodos | Rutas posibles |
|---------|---------------|
| 10 | 181,440 |
| 15 | 43,589,145,600 |
| 20 | 6.08 × 10¹⁶ |
| 25 | 3.10 × 10²³ |

### Vehicle Routing Problem (VRP)

Extensión del TSP con múltiples vehículos de capacidad `Q` y depósito central:

```
min Σ Σ w(i,j) × x_ijk
    k  (i,j)

sujeto a:
  Σ d_i × y_ik ≤ Q  ∀k   (restricción de capacidad)
  Σ y_ik = 1         ∀i≠0  (cada cliente visitado exactamente una vez)
```

---

## Algoritmo 1: Simulated Annealing

### Analogía cuántica: Quantum Tunneling

En mecánica cuántica, una partícula puede **atravesar una barrera de potencial** que clásicamente sería infranqueable. La probabilidad de tunneling es `P ∝ e^(-2κd)` donde `κ` y `d` dependen de la barrera.

SA emula este comportamiento: el sistema puede "saltar" a soluciones peores (atravesar barreras de energía) con probabilidad que decrece con el tiempo, permitiendo escapar de óptimos locales.

### Pseudocódigo

```
FUNCIÓN SimulatedAnnealing(tour_inicial, T₀, α, max_iter):
    tour_actual ← tour_inicial
    costo_actual ← evaluar(tour_actual)
    mejor_tour ← tour_actual
    mejor_costo ← costo_actual
    T ← T₀

    PARA it = 1 HASTA max_iter:
        vecino ← generar_vecino(tour_actual)   # 2-opt o or-opt
        costo_vecino ← evaluar(vecino)
        ΔE ← costo_vecino - costo_actual

        SI ΔE < 0:                             # mejora directa
            tour_actual ← vecino
            costo_actual ← costo_vecino
        SINO SI random() < exp(-ΔE / T):       # quantum tunneling
            tour_actual ← vecino               # aceptar movimiento peor
            costo_actual ← costo_vecino

        SI costo_actual < mejor_costo:
            mejor_tour ← tour_actual
            mejor_costo ← costo_actual

        T ← T × α                             # enfriamiento

    RETORNAR mejor_tour, mejor_costo
```

### Movimientos de vecindad

**2-opt:** Invierte un subsegmento de la ruta.
```
Antes: [0, 1, 2, 3, 4, 5, 0]
         ↕ invertir [2..4]
Después: [0, 1, 4, 3, 2, 5, 0]
```

**Or-opt:** Reinserta un nodo o segmento en otra posición.
```
Antes: [0, 1, 2, 3, 4, 5, 0]
         ↕ mover nodo 2 entre 4 y 5
Después: [0, 1, 3, 4, 2, 5, 0]
```

### Análisis de convergencia

La temperatura sigue un **schedule de enfriamiento geométrico**:
```
T(k) = T₀ × αᵏ
```

Para garantizar convergencia al óptimo global (en tiempo infinito), se requiere:
```
T(k) ≥ C / ln(k)    para alguna constante C
```

En la práctica, el enfriamiento geométrico con `α ∈ [0.95, 0.999]` ofrece excelentes resultados empíricos.

### Guía de parámetros

```
T₀ demasiado baja  → El sistema se congela pronto, queda en óptimo local
T₀ demasiado alta  → El sistema acepta todo, camina aleatoriamente

α muy pequeño (0.80) → Enfriamiento rápido, baja calidad, alta velocidad  
α muy grande (0.999) → Enfriamiento lento, alta calidad, tiempo largo

Regla práctica: T₀ tal que exp(-ΔE_promedio / T₀) ≈ 0.8 al inicio
```

---

## Algoritmo 2: Genetic Algorithm

### Analogía cuántica: Superposición y Medición

Un estado cuántico en superposición representa **múltiples posibilidades simultáneas**. Al medir, el estado colapsa a una solución específica. GA mantiene una población de soluciones (estados superpuestos) y evoluciona hacia el óptimo (colapso por selección).

### Operadores genéticos

#### Order Crossover (OX)

Preserva la propiedad de permutación sin repeticiones:

```
P1: [0, 1, 2 | 3, 4, 5 | 6, 7]
P2: [0, 3, 6 | 1, 7, 4 | 2, 5]
                ↓
Segmento de P1: [3, 4, 5]
Relleno de P2 (excluyendo {3,4,5}): [0, 6, 1, 7, 2]
Hijo: [_, _, _, 3, 4, 5, _, _] → rellenar con orden de P2
Hijo: [0, 6, 1, 3, 4, 5, 7, 2]  ✓ (permutación válida)
```

#### Mutación por swap

```python
# Con probabilidad p_mut = 0.12
i, j = random.sample(range(n), 2)
tour[i], tour[j] = tour[j], tour[i]
```

### Pseudocódigo

```
FUNCIÓN GeneticAlgorithm(tour_inicial, pop_size, generaciones):
    población ← generar_población(tour_inicial, pop_size)
    mejor_tour ← mejor_individuo(población)

    PARA g = 1 HASTA generaciones:
        elite ← seleccionar_top(población, k=pop_size/5)
        offspring ← []

        MIENTRAS len(offspring) < pop_size - len(elite):
            p1, p2 ← selección_torneo(población)
            hijo ← OX_crossover(p1, p2)
            SI random() < 0.12: hijo ← mutar(hijo)
            offspring.append(hijo)

        población ← ordenar(elite + offspring, por=costo)
        mejor_tour ← actualizar_mejor(población[0])

    RETORNAR mejor_tour
```

---

## Algoritmo 3: Ant Colony Optimization

### Analogía cuántica: Quantum Walk

Un **quantum walk** es la versión cuántica del random walk clásico. En lugar de seguir un único camino, la partícula explora múltiples caminos simultáneamente con amplitudes de probabilidad que interfieren constructiva o destructivamente.

ACO implementa esto mediante feromonas: los caminos más cortos acumulan más feromona (amplitud positiva), siendo seleccionados con mayor probabilidad en futuras iteraciones.

### Regla de transición probabilística

```
P(i → j) = [τ(i,j)]^α × [η(i,j)]^β
            ─────────────────────────────
            Σₖ [τ(i,k)]^α × [η(i,k)]^β

donde:
  τ(i,j) = feromona en arista (i,j)
  η(i,j) = 1/d(i,j)  (visibilidad, inverso de distancia)
  α = importancia de la feromona  (típico: 1.0–1.5)
  β = importancia de la distancia (típico: 2.0–5.0)
```

### Actualización de feromonas

**Evaporación:**
```
τ(i,j) ← (1 - ρ) × τ(i,j)     para todo (i,j)
```

**Depósito:**
```
τ(i,j) ← τ(i,j) + Σₖ Δτₖ(i,j)

donde Δτₖ(i,j) = Q / Lₖ  si la hormiga k usó arista (i,j)
                 0         en caso contrario
```

### Pseudocódigo

```
FUNCIÓN ACO(nodos, n_ants, iteraciones, α, β, ρ, Q):
    τ ← matriz_feromonas_inicial(nodos, valor=1.0)
    mejor_tour ← greedy_tour(nodos)
    mejor_costo ← evaluar(mejor_tour)

    PARA it = 1 HASTA iteraciones:
        soluciones ← []

        PARA hormiga = 1 HASTA n_ants:
            tour ← construir_tour_probabilistico(nodos, τ, α, β)
            costo ← evaluar(tour)
            soluciones.append((tour, costo))

            SI costo < mejor_costo:
                mejor_tour, mejor_costo ← tour, costo

        # Evaporar
        τ ← τ × (1 - ρ)

        # Depositar
        PARA (tour, costo) EN soluciones:
            PARA arista (i,j) EN tour:
                τ[i][j] += Q / costo
                τ[j][i] += Q / costo

    RETORNAR mejor_tour, mejor_costo
```

### Guía de parámetros ACO

| Parámetro | Rango típico | Efecto |
|-----------|-------------|--------|
| `α` (feromona) | 1.0 – 2.0 | Mayor → más explotación de rutas conocidas |
| `β` (distancia) | 2.0 – 5.0 | Mayor → más greedy, menos exploración |
| `ρ` (evaporación) | 0.3 – 0.6 | Mayor → olvido más rápido, más exploración |
| `Q` | 50 – 200 | Escala de depósito de feromona |
| `n_ants` | n – 3n | Más hormigas → mejor exploración, más lento |

---

## Comparativa de algoritmos

| Criterio | SA | GA | ACO |
|---------|:--:|:--:|:---:|
| Velocidad (n<20) | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Calidad de solución | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Facilidad de tuning | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| Paralelizable | ✗ | ✓ | ✓ |
| Adapta a cambios | ⭐⭐ | ⭐ | ⭐⭐⭐ |
| Memoria requerida | Baja | Media | Media |

**Recomendación por caso de uso:**
- **Prototipado rápido / demos:** Simulated Annealing
- **Instancias grandes con tiempo disponible:** Genetic Algorithm
- **Rutas que cambian dinámicamente:** Ant Colony Optimization

---

## Referencias

1. Kirkpatrick, S., Gelatt, C.D., Vecchi, M.P. (1983). *Optimization by Simulated Annealing*. Science, 220(4598), 671–680.
2. Dorigo, M., Gambardella, L.M. (1997). *Ant Colony System: A Cooperative Learning Approach to the Traveling Salesman Problem*. IEEE Transactions on Evolutionary Computation.
3. Goldberg, D.E. (1989). *Genetic Algorithms in Search, Optimization and Machine Learning*. Addison-Wesley.
4. Arrazola, J.M. et al. (2020). *Quantum-inspired algorithms in practice*. Quantum, 4, 307.
