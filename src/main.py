import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from routes.modules import router as modules_router
from routes.groups import router as groups_router


def get_application():
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup():
        await config.database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await config.database.disconnect()

    app.include_router(modules_router, prefix="/modules")
    app.include_router(groups_router, prefix="/groups")

    return app


api = get_application()

if __name__ == "__main__":
    uvicorn.run("main:api", host='0.0.0.0', port=config.APP_PORT, reload=False, workers=3)
