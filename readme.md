# El Hogar del Hobbit

Plataforma web ficticia de ocio alternativo: tienda online de cartas coleccionables, juegos de mesa y rol, calendario de eventos y torneos, y foro de comunidad.
Proyecto académico de Gestión de Proyectos Software de la UEx · Grupo GB04. **Todos los datos son ficticios.**

## Contenido del repositorio

| Carpeta | Contenido |
|---|---|
| `Proyecto/` | Código de la aplicación con Flask y SQLite |
| `specs/` | Misión, objetivos y especificación de cada épica |
| `docs/` | Calidad, planificación y revisiones |

La gestión del proyecto está en la Wiki del repositorio.

## Tecnología

| Parte | Tecnología |
|---|---|
| Lenguaje | Python 3.10 o superior |
| Servidor web | Flask 3 |
| Base de datos | SQLite, un archivo local que no hay que instalar |
| Interfaz | Plantillas HTML con Jinja y CSS |
| Pruebas | pytest |

## Instalación y arranque

El código está en la carpeta **`Proyecto/`** del repositorio. Abre el terminal de VS Code en la raíz del repositorio y entra en ella:

```powershell
cd Proyecto
```

Todos los comandos siguientes se ejecutan **dentro de `Proyecto/`**.

```powershell
# 1. Crear el entorno virtual, solo la primera vez
py -m venv .venv

# 2. Instalar las dependencias, la primera vez y cuando cambie requirements.txt
.venv\Scripts\python -m pip install -r requirements.txt

# 3. Arrancar la web
.venv\Scripts\python run.py
```

Abrir **http://127.0.0.1:5000** en el navegador. Para pararla: `Ctrl + C`.

En Linux o macOS, usar `python3 -m venv .venv` y `.venv/bin/python` en lugar de `.venv\Scripts\python`.

### Pruebas

```powershell
.venv\Scripts\python -m pytest
```

### Base de datos

- Se crea sola al arrancar en `instance/hobbit.sqlite`. No se sube a GitHub, cada uno tiene la suya.
- En cada arranque se crean las tablas que falten y se cargan los datos ficticios que falten.
- Si se cambia una tabla que ya existía, por ejemplo al añadir una columna, hay que crearla de nuevo:

```powershell
.venv\Scripts\python -m flask --app run init-db
```

## Arquitectura

Aplicación web por capas. Las rutas de este apartado son relativas a la carpeta `Proyecto/`. Cada petición recorre las capas en este orden:

```
Navegador → routes/ → gestores/ → repositories/ → SQLite
                ↓
        templates/ + static/ → página HTML
```

| Capa | Carpeta | Qué contiene | Subtareas de Jira |
|---|---|---|---|
| Interfaz | `app/templates/`, `app/static/` | Páginas HTML y estilos | «Desarrollar la interfaz de…» |
| Presentación | `app/routes/` | Recibe la petición, llama al gestor y devuelve la página | Interfaz |
| Lógica de negocio | `app/gestores/` | Los gestores del diagrama de clases: reglas, validaciones y permisos | «Desarrollar la lógica y los datos de…» |
| Acceso a datos | `app/repositories/` | Consultas SQL | Lógica y datos |
| Base de datos | `app/database/schema/`, `app/database/seeds/` | Tablas y datos ficticios | Lógica y datos |
| Pruebas | `tests/` | Pruebas automáticas con pytest | Todas |

### Estructura de carpetas

```
Repositorio
├── readme.md                    # este documento
├── specs/                       # especificaciones del producto y de cada épica
├── docs/                        # calidad, planificación y revisiones
└── Proyecto/                    # código de la aplicación
    ├── app/
    │   ├── __init__.py          # crea la aplicación y registra las rutas automáticamente
    │   ├── db.py                # conexión con SQLite
    │   ├── routes/              # un archivo por módulo
    │   ├── gestores/            # un gestor por módulo, según el diagrama de clases
    │   ├── repositories/        # un archivo por tabla o módulo
    │   ├── database/
    │   │   ├── schema/          # tablas: 00_base.sql, 10_catalogo.sql…
    │   │   └── seeds/           # datos ficticios: 00_base.sql, 10_catalogo.sql…
    │   ├── templates/           # base.html, inicio.html, una carpeta por módulo
    │   └── static/css/          # estilos
    ├── tests/                   # una prueba por módulo
    ├── run.py                   # arranca la web
    └── requirements.txt         # dependencias
```

### Archivos SQL

Cada módulo crea sus tablas y sus datos en su propio archivo SQL, numerado: 00 base, 10 catálogo, 20 eventos, 30 foro, 40 usuarios, 50 notificaciones, 60 inventario y 70 soporte.

## Cómo añadir una historia nueva

Cada historia crea **sus propios archivos**. Así casi nunca hay conflictos al hacer merge. Ejemplo con US-01 Ver catálogo:

| # | Archivo | Qué poner |
|---|---|---|
| 1 | `app/database/schema/10_catalogo.sql` | `CREATE TABLE IF NOT EXISTS productos (...)` |
| 2 | `app/database/seeds/10_catalogo.sql` | `INSERT OR IGNORE INTO productos (id, ...) VALUES (1, ...)`, siempre con `id` fijo |
| 3 | `app/repositories/productos_repo.py` | Funciones con las consultas SQL |
| 4 | `app/gestores/gestor_catalogo.py` | Implementar `getProductos()` y `getProductosDisponibles()`, que ya existen y ahora lanzan `NotImplementedError` |
| 5 | `app/routes/catalogo.py` | `bp = Blueprint("catalogo", __name__)` y sus rutas. **Se registra solo** |
| 6 | `app/templates/catalogo/lista.html` | Página que empieza con `{% extends "base.html" %}` |
| 7 | `tests/test_catalogo.py` | Pruebas de los criterios de aceptación |

Para mostrar mensajes de carga, error o éxito: `flash("texto", "exito")`, `flash("texto", "error")` o `flash("texto", "info")`. La plantilla base ya los muestra.

## Reglas comunes

- Solo datos ficticios. Nunca datos personales reales.
- Toda página hereda de `base.html`, que ya incluye el menú, la accesibilidad básica y los mensajes.
- Antes de hacer commit: arrancar la web y pasar `pytest`. Todas las pruebas deben pasar.
- Las pruebas usan una base de datos temporal, así que nunca tocan la tuya.

## Flujo de trabajo con GitFlow y Jira

| Rama | Uso |
|---|---|
| `main` | Versiones entregadas: R1, R2 y R3 |
| `develop` | Integración de las historias terminadas |
| `feature/GB04-X-nombre` | Una por historia o tarea, creada desde Jira a partir de `develop` |

- Un único commit por subtarea, en una línea: `GB04-X #time 2h #comment Qué se ha hecho #done`
- Merges siempre con `--no-ff`: primero `develop → feature` y después `feature → develop`. Sin `#time` en los commits de merge.
- Configuración, una vez por persona: `git config merge.ff false`
