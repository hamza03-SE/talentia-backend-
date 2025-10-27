from fastapi import FastAPI
from app.core.config import Settings, get_settings
from app.api.routes_auth import router as auth_router 
from app.api.routes_users import router as user_router
import uvicorn 

setting = Settings()


app = FastAPI(
    title=setting.PROJECT_NAME,
    version=setting.VERSION,
    debug=setting.DEBUG,
)

app.include_router(auth_router, prefix=f"{setting.API_PREFIX}", tags=["auth"])
app.include_router(user_router, prefix=f"{setting.API_PREFIX}/users", tags=["Users"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
