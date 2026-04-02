# Guía: Subir QuantRoute a GitHub

Sigue estos pasos exactos para publicar el repositorio de Skila.

---

## Paso 1 — Crear la cuenta / organización en GitHub

1. Ve a [github.com](https://github.com) e inicia sesión
2. Para crear la organización de Skila:
   - Clic en tu avatar (esquina superior derecha)
   - **Settings → Organizations → New organization**
   - Nombre: `skila-academy` (o el que prefieras)
   - Plan: **Free** es suficiente para empezar

---

## Paso 2 — Crear el repositorio

1. En la organización, clic en **New repository**
2. Configurar:
   - **Repository name:** `quantroute`
   - **Description:** `Quantum-Inspired Route & Resource Optimization Engine`
   - Visibilidad: **Public** (para máxima visibilidad en el hackathon)
   - ✅ Add a README file: **NO** (ya lo tenemos)
   - ✅ Add .gitignore: **Python**
   - License: **MIT**
3. Clic en **Create repository**

---

## Paso 3 — Inicializar el repositorio local

Abre tu terminal en la carpeta del proyecto:

```bash
# Entrar a la carpeta del proyecto
cd quantroute

# Inicializar git
git init

# Agregar el remote (reemplaza USUARIO con tu nombre de organización)
git remote add origin https://github.com/skila-academy/quantroute.git
```

---

## Paso 4 — Agregar todos los archivos

Estructura final del repositorio:

```
quantroute/
├── README.md           ← README principal (el que generamos)
├── ALGORITHMS.md       ← Documentación técnica de algoritmos
├── CONTRIBUTING.md     ← Guía de contribución
├── LICENSE             ← MIT License
├── backend/
│   ├── main.py
│   └── requirements.txt
└── frontend/
    └── index.html
```

```bash
# Copiar los archivos de documentación a la raíz del proyecto
# (README.md, ALGORITHMS.md, CONTRIBUTING.md, LICENSE)

# Agregar todos los archivos
git add .

# Primer commit
git commit -m "feat: initial release — QuantRoute v1.0.0

- Quantum-inspired route optimization engine
- Algorithms: Simulated Annealing, Genetic Algorithm, ACO
- Modes: TSP, VRP, Resource Assignment
- FastAPI backend + standalone HTML frontend
- Built by Skila — Strategic Knowledge & Learning Academy"

# Subir al repositorio
git branch -M main
git push -u origin main
```

---

## Paso 5 — Configurar el repositorio en GitHub

Una vez subido, configura estos detalles en la página del repo:

### About (sidebar derecho)
- **Description:** `Quantum-Inspired Route & Resource Optimization Engine`
- **Website:** (tu sitio web de Skila cuando lo tengas)
- **Topics (tags):**
  ```
  optimization  quantum-inspired  logistics  simulated-annealing
  genetic-algorithm  ant-colony  vehicle-routing  python  fastapi
  operations-research  heuristics
  ```

### Settings → General
- ✅ Discussions: activar para comunidad
- ✅ Issues: activar para reportes de bugs

---

## Paso 6 — GitHub Pages (demo online opcional)

Para que el frontend sea accesible como demo en vivo:

1. Ve a **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` / folder: `/frontend`
4. La demo estará en: `https://skila-academy.github.io/quantroute/`

---

## Paso 7 — Crear el primer Release

1. En el repositorio → **Releases → Create a new release**
2. Tag: `v1.0.0`
3. Title: `QuantRoute v1.0.0 — Initial Release`
4. Description:
   ```
   ## QuantRoute v1.0.0 🎉
   
   Primera versión pública de nuestro motor de optimización quantum-inspired.
   
   ### ✨ Features
   - Simulated Annealing con criterio de Metropolis
   - Genetic Algorithm con crossover OX
   - Ant Colony Optimization con actualización de feromonas
   - Tres modos: TSP, VRP, Asignación de recursos
   - Frontend standalone sin dependencias de build
   - API REST con FastAPI + documentación automática
   
   ### 🔧 Stack
   Python 3.10+ · FastAPI · NumPy · HTML/CSS/JS · Canvas 2D
   ```
5. Adjuntar el ZIP del proyecto
6. **Publish release**

---

## Resultado esperado

Tu repositorio quedará así:
`github.com/skila-academy/quantroute`

Con:
- README profesional con badges, benchmarks y documentación completa
- Código limpio y comentado
- Licencia MIT
- Tags de descubrimiento correctos
- Demo en vivo via GitHub Pages
