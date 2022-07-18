from fastapi import APIRouter, Response, status
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet
from starlette.status import HTTP_204_NO_CONTENT

key = Fernet.generate_key()
f = Fernet(key)
user = APIRouter()


@user.get("/users", response_model=list[User], tags=["users"])
def get_users():
    # return "hello world"
    return conn.execute(users.select()).fetchall()


@user.post("/users", response_model=User, tags=["users"])
def create_users(user: User):
    new_user = {"name": user.name, "email": user.email}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    result = conn.execute(users.insert().values(new_user))
    print(result.lastrowid)
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()


@user.get("/users/{id}", response_model=User, tags=["users"])
def get_users_by_id(id: str):
    return conn.execute(users.select().where(users.c.id == id)).first()


@user.delete("/users/{id}", status_code= status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: str):
    conn.execute(users.delete().where(users.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)


@user.put("/users/{id}", response_model=User, tags=["users"])
def update_users(id: str, user: User):
    conn.execute(users.update().values(name=user.name,
                 email=user.email, 
                 password=f.encrypt(user.password.encode("utf-8"))
    ).where(users.c.id == id))
    return conn.execute(users.select().where(users.c.id == id)).first()