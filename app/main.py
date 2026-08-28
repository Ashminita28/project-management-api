from fastapi import FastAPI

app = FastAPI(
    title="Project Management API",
    description="Backend API for managing projects and tasks.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "message": "API is running"}
