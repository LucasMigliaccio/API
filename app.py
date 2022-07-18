from fastapi import FastAPI
from routes.user import user


app = FastAPI(
        title= "API LM",
        description="a simple API management of users",
        openapi_tags=[{
            "name": "users",
            "description": "users routes"
        }]
)


app.include_router(user)

