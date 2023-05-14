from http import HTTPStatus
from datetime import timedelta
from fastapi import APIRouter, Request, HTTPException, status, Depends, Body

from sqlalchemy.orm import Session

from apps import crud, models, schemas
from apps.api import deps
from apps.core.config import settings
from apps.core.security import create_access_token, verify_password

router = APIRouter()


@router.post("/register", response_model=schemas.UserGet)
async def register(request: Request, db: Session = Depends(deps.get_db), *, new_user: schemas.UserCreate):
    # if email already being used
    if crud.user.get_by_email(db, email=new_user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This email is already used")
    user = crud.user.create(db, obj_in=new_user)

    return user


@router.post("/login/access-token", response_model=schemas.ResponseToken)
async def login_access_token(request: Request, db: Session = Depends(deps.get_db), *, email: str, password: str):
    user = crud.user.authenticate(
        db, email=email, password=password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = schemas.ResponseToken(
        access_token=create_access_token(
            {"sub": user.json()}, expires_delta=access_token_expires),
        token_type="Bearer",
        status=status.HTTP_200_OK
    )
    return access_token


@router.post('/login-google/access-token', response_model=schemas.ResponseToken)
async def authenticate_google(request: Request, db: Session = Depends(deps.get_db), *, token: dict):
    if not crud.user.get_by_email(db, email=token.get('email')):
        created = schemas.UserCreate(
            displayname=token.get('given_name'),
            email=token.get('email'),
            user_type=schemas.UserType.google
        )
        crud.user.create(db, obj_in=created)
    user = crud.user.authenticate(
        db, email=token.get('email'), type=schemas.UserType.google
    )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = schemas.ResponseToken(
        access_token=create_access_token(
            {"sub": user.json()}, expires_delta=access_token_expires),
        token_type="Bearer",
        status=status.HTTP_200_OK
    )
    return access_token


@router.get('/me', response_model=schemas.UserGet)
async def get_me(request: Request):
    return schemas.UserGet.parse_obj(request.state.token_sub)


@router.put('/me/update')
async def update_me(request: Request, db: Session = Depends(deps.get_db), *, user_update: schemas.UserUpdateProfile):
    user_id = request.state.token_sub.get('id')
    user = crud.user.get(db, id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Prepare the update data
    update_data = user_update.dict(exclude_unset=True)
    updated_user = crud.user.update(db, db_obj=user, obj_in=update_data)

    return updated_user


@router.put('/me/change-password')
async def update_password(request: Request, db: Session = Depends(deps.get_db), *, password_update: schemas.UserUpdatePassword):
    user_id = request.state.token_sub.get('id')
    user = crud.user.get(db, id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Verify old password
    if not verify_password(password_update.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    # Update password
    updated_user = crud.user.update(db, db_obj=user, obj_in=password_update)

    return updated_user


@router.get('/me/reset-password')
# TODO: reset password, user forgot password
async def reset_password(request: Request, db: Session = Depends(deps.get_db), *, password_reset: schemas.UserResetPassword):
    # send reset token to user
    return  # ? notice to make user check email


@router.put('/me/reset-password/consent?={password_reset.reset_token}')
# TODO: reset password, user forgot password
async def reset_password(request: Request, db: Session = Depends(deps.get_db), *, password_reset: schemas.UserResetPassword):
    # verify reset token
    # update password if verified
    return


@router.delete('/delete', tags=["Debugs"])
async def delete_user(db: Session = Depends(deps.get_db), *, id: str):
    return crud.user.remove(db, id=id)


@router.get('/fetch', tags=["Debugs"])
async def fetch_user(db: Session = Depends(deps.get_db), *, email: str):
    return crud.user.get_by_email(db, email=email)
