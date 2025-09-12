
En el archivo `config.json` se encuentran todos los **hiperparámetros** que controlan el comportamiento del algoritmo genético utilizado para recrear imágenes mediante triángulos.

## 📌 Uso
1. Editar el archivo `config.json` con los valores deseados.
2. Ejecutar el programa principal del algoritmo genético.  
   El programa leerá automáticamente esta configuración y aplicará los parámetros.

---

### Población
- **`n_population_size`**: tamaño de la población inicial de individuos.

---

### Selección
- **`selection_method`**: método de selección de padres. Opciones:
  - `elite`
  - `roulette`
  - `universal`
  - `ranking`
  - `boltzmann`
  - `deterministic_tournaments`
  - `probabilistic_tournaments`

- **`k_selection_size`**: cantidad de padres seleccionados y de hijos generados en cada generación.

#### Selección por Boltzmann
- **`temperature_c`**: factor de enfriamiento.
- **`temperature_0`**: temperatura inicial.
- **`k_constant`**: constante de ajuste en el cálculo de probabilidades.
- **`t_generation`**: frecuencia de actualización de la temperatura (en generaciones).

#### Torneos
- **`m_selection_size`**: cantidad de individuos seleccionados al azar de la población para torneos determinísticos.
- **`threshold`**: probabilidad de elegir al mejor en torneos probabilísticos (`[0.5, 1]`).

---

### Cruza
- **`crossover_method`**: método de recombinación. Opciones:
  - `one_point`
  - `two_point`
  - `annular`
  - `uniform`

- **`crossover_probability`**: probabilidad de recombinación.
- **`p_uniform`**: probabilidad de intercambio de genes en cada posición (sólo para `uniform`).

---

### Mutación
- **`mutation_method`**: método de mutación. Opciones:
  - `gene`
  - `multigen_limited`
  - `multigen_uniform`
  - `complete`

- **`mutation_probability`**: probabilidad de mutación por individuo.
- **`mutation_M`**: número máximo de genes que pueden mutar en `multigen_limited`.

---

### Reemplazo de generaciones
- **`implementation`**: criterio para generar la nueva población:
  - `traditional`: reemplazo clásico.
  - `young-bias`: favorece a los individuos más jóvenes.

---

### Condiciones de corte
- **`stop_condition`**: criterio de finalización. Opciones:
  - `max_generations`
  - `max_time_seconds`
  - `acceptable_solution`
  - `structure`
  - `content`

#### Parámetros por condición
- **`stop_condition_max_time_seconds`**: tiempo máximo en segundos.
- **`stop_condition_max_generations`**: número máximo de generaciones.
- **`stop_condition_acceptable_solution`**: fitness mínimo aceptable (0 a 1).

- **`stop_condition_structure_generations`**: número de generaciones a revisar cambios en estructura.
- **`stop_condition_structure_percentage`**: porcentaje de variación esperado.
- **`stop_condition_structure_delta`**: tolerancia de variación.

- **`stop_condition_content_generations`**: número de generaciones a revisar cambios en contenido.
- **`stop_condition_content_delta`**: tolerancia de variación en contenido.

---
