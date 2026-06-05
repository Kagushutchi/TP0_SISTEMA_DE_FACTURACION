from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import clientes, productos, facturas, reportes

app = FastAPI(
    title="Sistema de Facturación - API Políglota",
    description="TPO Base de Datos 2 - Integración MySQL + MongoDB",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes.router)
app.include_router(productos.router)
app.include_router(facturas.router)
app.include_router(reportes.router)


@app.get("/")
def root():
    return {
        "mensaje": "API Sistema de Facturación",
        "documentacion": "/docs",
        "bases": ["MySQL (clientes, productos, teléfonos)", "MongoDB (facturas con items embebidos)"],
    }
