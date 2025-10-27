from fastapi import FastAPI
from app.core.config import Settings, get_settings
from app.api.routes_auth import router as auth_router  # ✅ nouveau nom
import uvicorn

setting = Settings()


app = FastAPI(
    title=setting.PROJECT_NAME,
    version=setting.VERSION,
    debug=setting.DEBUG,
)

app.include_router(auth_router, prefix=f"{setting.API_PREFIX}", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
