from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from database import engine

# Routers
from routers.roles import router as roles_router
from routers.usuarios import router as usuarios_router
from routers.acudientes import router as acudientes_router
from routers.estudiantes import router as estudiantes_router
from routers.conductores import router as conductores_router
from routers.vehiculos import router as vehiculos_router
from routers.rutas import router as rutas_router
from routers.paraderos import router as paraderos_router
from routers.estudiante_ruta import router as estudiante_ruta_router
from routers.registros_abordaje import router as registros_abordaje_router


app = FastAPI(
    title="Gestión de Rutas y Transporte Escolar",
    description="API para la gestión del transporte escolar",
    version="1.0.0"
)

# Permite abrir el frontend desde FastAPI o desde un servidor local distinto
# durante el desarrollo. La base de datos continúa protegida detrás de la API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500", "http://127.0.0.1:5500",
        "http://localhost:8443", "http://127.0.0.1:8443",
        "http://192.168.1.10:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# REGISTRO DE ROUTERS
# =========================

app.include_router(roles_router)
app.include_router(usuarios_router)
app.include_router(acudientes_router)
app.include_router(estudiantes_router)
app.include_router(conductores_router)
app.include_router(vehiculos_router)
app.include_router(rutas_router)
app.include_router(paraderos_router)
app.include_router(estudiante_ruta_router)
app.include_router(registros_abordaje_router)


# =========================
# RUTA PRINCIPAL
# =========================

BASE_DIR = Path(__file__).resolve().parent


@app.get("/", include_in_schema=False)
def inicio():
    """Entrega la interfaz web; Swagger se conserva disponible en /docs."""
    return FileResponse(BASE_DIR / "index.html")


@app.get("/style.css", include_in_schema=False)
def estilos():
    return FileResponse(BASE_DIR / "style.css", media_type="text/css")


@app.get("/app.js", include_in_schema=False)
def interfaz_js():
    return FileResponse(BASE_DIR / "app.js", media_type="application/javascript")


# =========================
# PRUEBA DE BASE DE DATOS
# =========================

@app.get("/prueba-db")
def prueba_db():
    with engine.connect() as connection:
        resultado = connection.execute(text("SELECT 1"))

        return {
            "mensaje": "Conexion con Supabase exitosa",
            "resultado": resultado.scalar()
        }
