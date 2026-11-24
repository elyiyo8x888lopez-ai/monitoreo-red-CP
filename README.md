# Sistema de Monitoreo de Infraestructura de Red - CP

Agente automatizado para la deteccion de fallas en tiempo real, analisis de impacto en cascada y notificacion de incidentes sobre topologias jerarquicas (Switch Capa 3, Routers de edificio y subredes VLAN).

## Requisitos
- Python 3.10+
- Librerias listadas en `requirements.txt`

## Instalacion local
1. Clonar el repositorio.
2. Crear y activar el entorno virtual:
   `python3 -m venv venv && source venv/bin/activate`
3. Instalar dependencias:
   `pip install -r requirements.txt`
4. Copiar `.env.example` a `.env` y configurar credenciales.