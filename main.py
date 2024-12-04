from fastapi import FastAPI
from config.db import engine, Base
from routes import userRoutes, monitorRoutes
from fastapi.middleware.cors import CORSMiddleware


#Base.metadata.create_all(bind=engine)
app = FastAPI(title="Monitor Columna", description="Sistema de monitoreo lumbar", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(userRoutes.router, tags=["User"])
app.include_router(monitorRoutes.router, tags=["Monitor"])

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello World"}

