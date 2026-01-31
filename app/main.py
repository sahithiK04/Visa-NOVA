from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.upload import router as upload_router
from app.routes.transactions import router as transactions_router

# 🔴 FIRST: create the FastAPI app
app = FastAPI(title="VISA-NOVA")

# 🔴 THEN: add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔴 THEN: include routers
app.include_router(upload_router)
app.include_router(transactions_router)

@app.get("/")
def health():
    return {"status": "VISA-NOVA running"}
