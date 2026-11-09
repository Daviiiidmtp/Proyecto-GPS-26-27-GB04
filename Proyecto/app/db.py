"""Conexión con la base de datos SQLite.

- Las tablas se definen en app/database/schema/*.sql
- Los datos ficticios se cargan desde app/database/seeds/*.sql
Los archivos se ejecutan en orden alfabético (por eso empiezan por un número).
"""
import sqlite3
from pathlib import Path

import click
from flask import current_app, g

CARPETA_BD = Path(__file__).parent / "database"


def get_db():
    """Devuelve la conexión de la petición actual (la crea si no existe)."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row  # permite usar fila["nombre"]
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(error=None):
    """Cierra la conexión al terminar cada petición."""
    conexion = g.pop("db", None)
    if conexion is not None:
        conexion.close()


def _ejecutar_carpeta(conexion, carpeta):
    for fichero in sorted(carpeta.glob("*.sql")):
        conexion.executescript(fichero.read_text(encoding="utf-8"))


def init_db():
    """Crea las tablas que falten y carga los datos ficticios que falten.

    Se ejecuta en cada arranque. Por eso:
    - las tablas usan CREATE TABLE IF NOT EXISTS
    - los datos usan INSERT OR IGNORE con id fijo
    """
    conexion = get_db()
    _ejecutar_carpeta(conexion, CARPETA_BD / "schema")
    _ejecutar_carpeta(conexion, CARPETA_BD / "seeds")
    conexion.commit()


@click.command("init-db")
def init_db_command():
    """Borra la base de datos local y la crea de nuevo desde cero."""
    close_db()
    ruta = Path(current_app.config["DATABASE"])
    if ruta.exists():
        ruta.unlink()
    init_db()
    click.echo("Base de datos creada de nuevo con los datos de ejemplo.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    with app.app_context():
        init_db()
