# El Hogar del Hobbit

Plataforma web ficticia de ocio alternativo: tienda online (cartas coleccionables, juegos de mesa y rol), calendario de eventos y torneos, y foro de comunidad.
Proyecto académico de Gestión de Proyectos Software (UEx) · Grupo GB04. **Todos los datos son ficticios.**

## Tecnología

| Parte | Tecnología |
|---|---|
| Lenguaje | Python 3.10 o superior |
| Servidor web | Flask 3 |
| Base de datos | SQLite (un archivo local; no hay que instalar nada) |
| Interfaz | Plantillas HTML (Jinja) + CSS |
| Pruebas | pytest |

## Instalación y arranque

Desde la carpeta del proyecto, en el terminal de VS Code (PowerShell):

```powershell
# 1. Crear el entorno virtual (solo la primera vez)
py -m venv .venv

# 2. Instalar las dependencias (la primera vez y cuando cambie requirements.txt)
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

- Se crea sola al arrancar, en `instance/hobbit.sqlite` (no se sube a GitHub; cada uno tiene la suya).
- En cada arranque se crean las tablas que falten y se cargan los datos ficticios que falten.
- Si se cambia una tabla que ya existía (por ejemplo, añadir una columna), hay que crearla de nuevo:

```powershell
.venv\Scripts\python -m flask --app run init-db
```

## Arquitectura

Aplicación web por capas. Cada petición recorre las capas en este orden:

```
Navegador → routes/ → gestores/ → repositories/ → SQLite
                ↓
        templates/ + static/ → página HTML
```

| Capa | Carpeta | Qué contiene | Subtareas de Jira |
|---|---|---|---|
| Interfaz (frontend) | `app/templates/`, `app/static/` | Páginas HTML y estilos | «Desarrollar la interfaz de…» |
| Presentación | `app/routes/` | Recibe la petición, llama al servicio y devuelve la página | Interfaz |
| Lógica de negocio | `app/gestores/` | Los gestores del diagrama de clases: reglas, validaciones y permisos | «Desarrollar la lógica y los datos de…» |
| Acceso a datos | `app/repositories/` | Consultas SQL | Lógica y datos |
| Base de datos | `app/database/schema/`, `app/database/seeds/` | Tablas y datos ficticios | Lógica y datos |
| Pruebas | `tests/` | Pruebas automáticas con pytest | Todas |

### Estructura de carpetas

```
├── app/
│   ├── __init__.py          # crea la aplicación y registra las rutas automáticamente
│   ├── db.py                # conexión con SQLite
│   ├── routes/              # un archivo por módulo (inicio.py, catalogo.py…)
│   ├── gestores/            # un gestor por módulo, según el diagrama de clases
│   ├── repositories/        # un archivo por tabla o módulo (productos_repo.py…)
│   ├── database/
│   │   ├── schema/          # tablas: 00_base.sql, 10_catalogo.sql…
│   │   └── seeds/           # datos ficticios: 00_base.sql, 10_catalogo.sql…
│   ├── templates/           # base.html, inicio.html, una carpeta por módulo
│   └── static/css/          # estilos
├── tests/                   # una prueba por módulo (test_catalogo.py…)
├── specs/                   # especificaciones (épicas e historias)
├── docs/                    # calidad (DoR, DoD), planificación y revisiones
├── run.py                   # arranca la web
└── requirements.txt         # dependencias
```

## Gestores (diagrama de clases)

La lógica sigue el diagrama de gestores del equipo. Los métodos **ya existen** en `app/gestores/` y lanzan `NotImplementedError` hasta que su historia los implementa. Cada historia **rellena sus métodos y no cambia los nombres**.

| Gestor | Archivo | Método | Historia |
|---|---|---|---|
| Gestor Catálogo | `gestor_catalogo.py` | `getProductos()`, `getProducto(idProducto)`, `getProductosDisponibles()` | US-01 |
| | | `getProductosPorNombre(nombre)` | US-02 |
| | | `getProductosPorTipo(tipo)` | US-03 |
| | | `anadirProductoCesta(idProducto, cantidad)`, `getCesta(idUsuario)` | US-16 |
| | | `realizarCompra(idUsuario)` | US-17 |
| | | `crearProducto(producto)` · @Admin | US-12 |
| | | `cambiarStock(idProducto, stock)` · @Admin | US-13 |
| Gestor Evento | `gestor_evento.py` | `getEventosDisponibles(tipoEvento=None)` | US-04 |
| | | `apuntarmeEnEvento(idEvento, idUsuario)` | US-05 |
| | | `crearEvento(evento)` · @Admin | US-06 |
| Gestión Foro | `gestor_foro.py` | `crearTema(titulo)`, `getTema(idTema)` | US-07 |
| | | `anadirComentario(idUsuario, idTema, comentario)` | US-08 |
| | | `eliminarMensaje(idMensaje)` · @Admin @Moderador | US-10 |
| Gestor Usuario | `gestor_usuario.py` | `crearUsuario(usuario)`, `getRolUsuario(idUsuario)` | US-09 |
| | | `cambiarRol(idUsuario, rol)`, `banearUsuario(idUsuario)` · @Admin @Moderador | US-10 |
| Soporte y Contacto | `gestor_soporte.py` | `reportarIncidencia(incidencia)` | US-14 |
| | | `getFaqs()` | US-15 |
| Notificaciones | — | Sin gestor: la interfaz las obtiene de `getEventosDisponibles()` | US-11 |

Diferencias con el diagrama, por cómo funciona Python:
- `getProductos(int idProducto)` se llama `getProducto(idProducto)`, porque Python no admite dos funciones con el mismo nombre.
- `getEventosDisponibles()` y `getEventosDisponibles(tipoEvento)` son una sola función con el parámetro opcional `tipoEvento`.
- `añadir…` se escribe `anadir…` (sin ñ) para evitar problemas de codificación.
- `getFaqs()` no estaba en el diagrama y es necesario para US-15.

### Números de los archivos SQL por módulo

Los archivos SQL se ejecutan en orden alfabético. Cada módulo usa su número, para no editar el mismo archivo que otro compañero:

| Número | Módulo | Épica |
|---|---|---|
| `00` | Base | — |
| `10` | Catálogo | EP-01 |
| `20` | Eventos | EP-02 |
| `30` | Foro | EP-03 |
| `40` | Usuarios | EP-04 |
| `50` | Notificaciones | EP-05 |
| `60` | Inventario | EP-06 |
| `70` | Soporte | EP-07 |

## Cómo añadir una historia nueva (ejemplo: US-01 Ver catálogo)

Cada historia crea **sus propios archivos**. Así casi nunca hay conflictos al hacer merge.

| # | Archivo | Qué poner |
|---|---|---|
| 1 | `app/database/schema/10_catalogo.sql` | `CREATE TABLE IF NOT EXISTS productos (...)` |
| 2 | `app/database/seeds/10_catalogo.sql` | `INSERT OR IGNORE INTO productos (id, ...) VALUES (1, ...)` (siempre con `id` fijo) |
| 3 | `app/repositories/productos_repo.py` | Funciones con las consultas SQL |
| 4 | `app/gestores/gestor_catalogo.py` | Implementar `getProductos()` y `getProductosDisponibles()` (ya existen; ahora lanzan `NotImplementedError`) |
| 5 | `app/routes/catalogo.py` | `bp = Blueprint("catalogo", __name__)` y sus rutas. **Se registra solo** |
| 6 | `app/templates/catalogo/lista.html` | Página que empieza con `{% extends "base.html" %}` |
| 7 | `tests/test_catalogo.py` | Pruebas de los criterios de aceptación |

Para mostrar mensajes de carga, error o éxito: `flash("texto", "exito")`, `flash("texto", "error")` o `flash("texto", "info")`. La plantilla base ya los muestra.

## Reglas comunes

- Solo datos ficticios (R-01). Nunca datos personales reales.
- Toda página hereda de `base.html`, que ya incluye el menú, la accesibilidad básica (idioma, salto al contenido, foco visible) y los mensajes.
- Antes de hacer commit: arrancar la web y pasar `pytest`. Todas las pruebas deben pasar.
- Las pruebas usan una base de datos temporal, así que nunca tocan la tuya.

## Flujo de trabajo (GitFlow + Jira)

| Rama | Uso |
|---|---|
| `main` | Versiones entregadas (R1, R2, R3) |
| `develop` | Integración de las historias terminadas |
| `feature/GB04-X-nombre` | Una por historia o tarea, creada desde Jira a partir de `develop` |

- Un único commit por subtarea, en una línea: `GB04-X #time 2h #comment Qué se ha hecho #done`
- Merges siempre con `--no-ff`: primero `develop → feature` y después `feature → develop`. Sin `#time` en los commits de merge.
- Configuración, una vez por persona: `git config merge.ff false`
