from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import vuelos_api

app = FastAPI(title="Gestión de Vuelos - API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vuelos_api.router, prefix="/api", tags=["Vuelos"])

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de Gestión de Vuelos"}
