from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import create_tables
from routes.reviews import router as reviews_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Tables created")
    yield
    print("Shutting down")


app = FastAPI(
    lifespan=lifespan,
    title="Rangmanch API",
    description="API for Rangmanch",
    version="0.0.1",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# routers
app.include_router(reviews_router)


@app.get("/")
def root():
    return {"message": "Hello World"}
