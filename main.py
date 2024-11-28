import uvicorn
from fastapi import FastAPI
from database import engine, Base
from routers import mission as MissionRouter
from routers import spy_cat as SpycatRouter
from routers import target as TargetRouter

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(SpycatRouter.spy_cat, prefix="/spy_cat")
app.include_router(MissionRouter.mission, prefix="/mission")
app.include_router(TargetRouter.target, prefix="/target")


if __name__ == '__main__':
    uvicorn.run("main:app", host='localhost', port=8080, reload=True)
