from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import alerts

app = FastAPI(
    title="Hybrid NIDS API & Dashboard Server",
    description="Backend API phục vụ quan sát lưu lượng mạng, alerts thời gian thực và quản lý rules",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alerts.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "NIDS_API"}
