from fastapi import FastAPI
from routes.api_router import api_router
#from config.openapi import tags_metadata

app = FastAPI(
    title="Mascotas API",
    description="a REST API using python and postgreSQL",
    version="0.0.1",
    #openapi_tags=tags_metadata,
)

app.include_router(api_router)
