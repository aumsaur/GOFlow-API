from datetime import timedelta
from fastapi import APIRouter, Request, HTTPException, status, Depends, Body

from sqlalchemy.orm import Session

from apps import crud, schemas
from apps.api import deps
from apps.core.config import settings
from apps.core.security import create_access_token, verify_password

router = APIRouter()


@router.post("/register", response_model=schemas.UserGet)
async def register(request: Request, db: Session = Depends(deps.get_db), *, new_user: schemas.UserCreate):
    """
    Register a new user.

    Parameters:
    - request (Request): The request object.
    - db (Session, optional): The database session (provided by dependency injection).
    - new_user (schemas.UserCreate): The user data for registration.

    Returns:
    - schemas.UserGet: The registered user.

    Raises:
    - HTTPException(409): If the email is already used.

    Example:
    ```
    POST /register
    Request Body:
    {
        "new_user": {
            "displayname": "user" (Optional),
            "email": "user@example.com",
            "password": "password123"
        }
    }
    ```
    """
    # new_user email is duplicated with database
    if crud.user.get_by_email(db, email=new_user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This email is already used")
    if (not new_user.display_name):
        new_user.display_name = new_user.email.split("@")[0]

    user = crud.user.create(db, obj_in=new_user)

    return user


@router.post("/login/access-token", response_model=schemas.ResponseToken)
async def login_access_token(request: Request, db: Session = Depends(deps.get_db), *, email: str = Body(...), password: str = Body(...)):
    """
    Authenticate user and generate an access token.

    Parameters:
    - request (Request): The request object.
    - db (Session, optional): The database session (provided by dependency injection).
    - email (str, Body): The user's email.
    - password (str, Body): The user's password.

    Returns:
    - schemas.ResponseToken: The generated access token.

    Raises:
    - HTTPException(401): If the email or password is incorrect.

    Example:
    ```
    POST /login/access-token
    Request Body:
    {
        "email": "test@example.com",
        "password": "password123"
    }
    ```
    """
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
            {"sub": user.id}, expires_delta=access_token_expires),
        token_type="Bearer"
    )
    return access_token


@router.post('/login-google/access-token', response_model=schemas.ResponseToken)
async def authenticate_google(request: Request, db: Session = Depends(deps.get_db), *, token: dict):
    """
    Authenticate user with Google and generate an access token.

    Parameters:
    - request (Request): The request object.
    - db (Session, optional): The database session (provided by dependency injection).
    - token (dict, Body): The Google authentication token.

    Returns:
    - schemas.ResponseToken: The generated access token.

    Example:
    ```
    POST /login-google/access-token
    Request Body:
    {
        "token": {
            "id": "test@example.com",
            "given_name": "John"
            ...
        }
    }
    ```
    """
    if not crud.user.get_by_email(db, email=token.get('email')):
        created = schemas.UserCreate(
            display_name=token.get('given_name'),
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
            {"sub": user.id}, expires_delta=access_token_expires),
        token_type="Bearer"
    )
    return access_token


@router.get('/me', response_model=schemas.UserGet)
async def get_me(request: Request, db: Session = Depends(deps.get_db)):
    """
    Get the authenticated user's profile.

    Parameters:
    - request (Request): The request object.
    - db (Session, optional): The database session (provided by dependency injection).

    Returns:
    - schemas.UserGet: The authenticated user's profile.

    Example:
    ```
    GET /me
    ```
    """
    user = crud.user.get(db, id=request.state.user_id)
    return schemas.UserGet.parse_obj(user)


@router.put('/me/update')
async def update_me(request: Request, db: Session = Depends(deps.get_db), *, user_update: schemas.UserUpdateProfile):
    """
    Update the authenticated user's profile.

    Parameters:
    - request (Request): The request object.
    - db (Session, optional): The database session (provided by dependency injection).
    - user_update (schemas.UserUpdateProfile): The updated user data.

    Returns:
    - The updated user.

    Raises:
    - HTTPException(404): If the user is not found.
    - HTTPException(403): If the user is not authorized to update the profile.

    Example:
    ```
    PUT /me/update
    Request Body:
    {
        "user_update": {
            "display_name": "John Doe"
            "email": "john.doe@example.com"
        }
    }
    ```
    """
    user = crud.user.get(db, id=request.state.user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id != user.get('id'):
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Prepare the update data
    update_data = user_update.dict(exclude_unset=True)
    updated_user = crud.user.update(db, db_obj=user, obj_in=update_data)

    return updated_user


@router.put('/me/change-password')
async def update_password(request: Request, db: Session = Depends(deps.get_db), *, password_update: schemas.UserUpdatePassword):
    """
    Update the authenticated user's password.

    Parameters:
    - request (Request): The request object.
    - db (Session, optional): The database session (provided by dependency injection).
    - password_update (schemas.UserUpdatePassword): The updated password data.

    Returns:
    - The updated user.

    Raises:
    - HTTPException(404): If the user is not found.
    - HTTPException(403): If the user is not authorized to update the password.
    - HTTPException(400): If the old password is incorrect.

    Example:
    ```
    PUT /me/change-password
    Request Body:
    {
        "password_update": {
            "old_password": "old_password123",
            "new_password": "new_password123"
        }
    }
    ```
    """
    user = request.state.user_id

    user = crud.user.get(db, id=user)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id != user.get('id'):
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


@router.delete('/delete')
async def delete_user(request: Request, db: Session = Depends(deps.get_db), *, confirm_str: str):
    user = request.state.token_sub
    # something to confirm that user want to remove this account
    return crud.user.remove(db, id=user.get('id'))


# @router.get('/fetch', tags=["Debugs"])
# async def fetch_user(db: Session = Depends(deps.get_db), *, email: str):
#     return crud.user.get_by_email(db, email=email)
