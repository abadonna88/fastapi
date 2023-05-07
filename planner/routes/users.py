from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn
from database.connection import Database


user_database = Database(User)
user_router = APIRouter(tags=["User"])
users = {}


@user_router.post("/d/signup")
async def sign_user_up(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already")
    
    await user_database.save(user)
    return {"message": "User created successfully"}


@user_router.post("/d/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if not user_exist:
        raise HTTPException(status_code=statsu.HTTP_404_NOT_FOUND, detail="User with email does not exist")
    if user_exist.password == user.password:
        return {"message": "User signed in successfully"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid details passed")


@user_router.post("/signup")
async def sign_new_user(data: User) -> dict:
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exists"
        )
    users[data.email] = data
    return {"message": "User successfully registered!"}


@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    if user.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    if users[user.email].password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed"
        )
    return {"message": "User signed in successfully"} 
