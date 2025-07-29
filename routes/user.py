from fastapi import APIRouter, Depends, HTTPException, Body
from database.db_connection import get_connection
from User.user_utill import *
from database.schemas.users_schema import *
from Security.auth import get_current_user, create_access_token
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi import APIRouter, HTTPException , Query


router = APIRouter(prefix="/user" , tags=["User"])

@router.post("/signup")
def signup(payload: SignupRequest, db=Depends(get_connection)):
    success, msg = create_user(db, payload.name, payload.mobile, payload.email, payload.password)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}


@router.post("/login")
def login(payload: LoginRequest, db=Depends(get_connection)):
    if not payload.identifier or not payload.password:
        raise HTTPException(status_code=400, detail="Both identifier and password are required")

    success, result = login_user(db, payload.identifier, payload.password)
    if not success:
        raise HTTPException(status_code=401, detail=result)

    user = result["user"]
    token_data = {"id": user["id"]}
    token = create_access_token(token_data)

    return {
        "status": "success",
        "message": result["message"],
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/protected")
def protected_route(user: dict = Depends(get_current_user)):
    return {"message": "You are authorized", "user": user}

@router.put("/update-user-info", summary="Update info of logged-in user (JWT required)")
def update_user_info(
        payload: UpdateUserInfoRequest = Body(...),
        db=Depends(get_connection),
        current_user=Depends(get_current_user)
):
    user_id = current_user.get("id")

    # Fetch existing user info
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT name, mobile, email FROM users WHERE id = %s", (user_id))
        user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    success, result = update_user_info_by_identifier(
        db,
        identifier=user_id,
        password=payload.password,
        new_name=payload.new_name or user['name'],
        new_mobile=payload.new_mobile or user['mobile'],
        new_email=payload.new_email or user['email']
    )

    if success:
        return {"success": True, **result}
    return {"success": False, "error": result}


@router.post("/update-password", summary="Change password for current logged-in user (JWT required)")
def update_password(
        payload: UpdatePasswordRequest,
        db=Depends(get_connection),
        current_user=Depends(get_current_user)
):
    identifier = current_user.get("id")

    success, message = update_password_by_old_password(
        db,
        identifier=identifier,
        old_password=payload.old_password,
        new_password=payload.new_password
    )

    if success:
        return {"success": True, "message": message}
    return {"success": False, "error": message}


@router.post("/send-password-change-otp")
def send_otp(payload: IdentifierRequest, db=Depends(get_connection)):
    success, otp_or_msg = send_password_change_otp(db, payload.identifier)
    if success:
        return {"success": True, "otp": otp_or_msg}
    return {"success": False, "error": otp_or_msg}


@router.post("/change-password-by-otp")
def change_by_otp(payload: ChangePasswordByOTPRequest, db=Depends(get_connection)):
    success, msg = change_password_by_otp(
        db,
        mobile=payload.mobile,
        otp_code=payload.otp_code,
        new_password=payload.new_password
    )
    if success:
        return {"success": True, "message": msg}
    return {"success": False, "error": msg}


@router.delete("/delete", summary="Delete current logged-in user")
def delete_user(
        payload: DeleteUserRequest,
        db=Depends(get_connection),
        current_user=Depends(get_current_user)
):
    identifier = current_user.get("id")

    success, msg = delete_user_by_identifier(db, identifier, payload.password)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}


@router.get("/all-users", summary="Get all users (no JWT)")
def get_all_users(db=Depends(get_connection)):
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    return {"users": users}


@router.get("/users-by-identifier/{identifier}", summary="Get user by identifier (without password)")
def get_user_by_identifier(identifier: str, db=Depends(get_connection)):
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT id, name, mobile, email, is_active, created_at
            FROM users
            WHERE mobile = %s OR email = %s
        """, (identifier, identifier))
        user = cursor.fetchone()

    if not user:
        return {"error": "User not found"}
    return {"user": user}


@router.get("/me", summary="Get current logged-in user using JWT")
def get_me(db=Depends(get_connection), current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("id")
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT id, name, mobile, email, is_active, created_at
            FROM users WHERE id = %s
        """, (user_id,))
        user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user}





# from fastapi import APIRouter, Depends, HTTPException
# from database.db_connection import get_connection
# from User.user_utill import *
# from database.schemas.users_schema import *
#
# router = APIRouter(prefix="/user", tags=["User"])
#
#
# @router.post("/signup")
# def signup(payload: SignupRequest, db=Depends(get_connection)):
#     success, msg = create_user(db, payload.name, payload.mobile, payload.email, payload.password)
#     if not success:
#         raise HTTPException(status_code=400, detail=msg)
#     return {"message": msg}
#
#
# @router.post("/login")
# def login(payload: LoginRequest, db=Depends(get_connection)):
#     if not payload.identifier or not payload.password:
#         raise HTTPException(status_code=400, detail="Both identifier and password are required")
#
#     success, result = login_user(db, payload.identifier, payload.password)
#     if not success:
#         raise HTTPException(status_code=401, detail=result)
#
#     return {
#         "status": "success",
#         "message": result["message"],
#         "user": result["user"]
#     }
#
# # 3. Update User Info API
# @router.post("/update-user-info")
# def update_user_info(payload: UpdateUserInfoRequest, db=Depends(get_connection)):
#     success, result = update_user_info_by_identifier(
#         db,
#         identifier=payload.identifier,
#         password=payload.password,
#         new_name=payload.new_name,
#         new_mobile=payload.new_mobile,
#         new_email=payload.new_email
#     )
#     if success:
#         return {"success": True, **result}
#     return {"success": False, "error": result}
#
#
# @router.post("/update-password")
# def update_password(payload: UpdatePasswordRequest, db=Depends(get_connection)):
#     success, message = update_password_by_old_password(
#         db,
#         identifier=payload.identifier,
#         old_password=payload.old_password,
#         new_password=payload.new_password
#     )
#     if success:
#         return {"success": True, "message": message}
#     return {"success": False, "error": message}
#
# # ===========================================use when sms provider available ================================
#
#
# # @router.post("/send-password-change-otp-service")
# # def send_password_change_otp_api(payload: IdentifierRequest, db=Depends(get_connection)):
# #     success, message = send_password_change_otp_service(db, payload.identifier)
# #     if success:
# #         return {"success": True, "message": message}
# #     return {"success": False, "error": message}
# #
# #
# # @router.post("/verify-password-change-otp")
# # def verify_password_change_otp_api(payload: PasswordChangeByOtpRequest, db=Depends(get_connection)):
# #     success, message = verify_password_change_otp_and_update(
# #         db, payload.mobile, payload.otp_code, payload.new_password
# #     )
# #     if success:
# #         return {"success": True, "message": message}
# #     return {"success": False, "error": message}
#
# # ===========================================use when sms provider available ^^^================================
#
# # ============================================remove it when sms provider===========================================================
# @router.post("/send-password-change-otp")
# def send_otp(payload: IdentifierRequest, db=Depends(get_connection)):
#     success, otp_or_msg = send_password_change_otp(db, payload.identifier)
#     if success:
#         return {"success": True, "otp": otp_or_msg}  # Only show OTP in dev/testing
#     return {"success": False, "error": otp_or_msg}
#
#
# @router.post("/change-password-by-otp")
# def change_by_otp(payload: ChangePasswordByOTPRequest, db=Depends(get_connection)):
#     success, msg = change_password_by_otp(
#         db,
#         mobile=payload.mobile,
#         otp_code=payload.otp_code,
#         new_password=payload.new_password
#     )
#     if success:
#         return {"success": True, "message": msg}
#     return {"success": False, "error": msg}
#
# # ============================================remove it wehn sms provider ^^ ===========================================================
#
#
#
# @router.delete("/delete")
# def delete_user(payload: DeleteUserRequest, db=Depends(get_connection)):
#     success, msg = delete_user_by_identifier(db, payload.identifier, payload.password)
#     if not success:
#         raise HTTPException(status_code=400, detail=msg)
#     return {"message": msg}
#
#
# @router.get("/all-users", summary="Get all users (with password)")
# def get_all_users(db=Depends(get_connection)):
#     with db.cursor(dictionary=True) as cursor:
#         cursor.execute("SELECT * FROM users")
#         users = cursor.fetchall()
#     return {"users": users}
#
#
# @router.get("/users-by-identifier/{identifier}", summary="Get user by identifier (mobile or email), without password")
# def get_user_by_identifier(identifier: str, db=Depends(get_connection)):
#     with db.cursor(dictionary=True) as cursor:
#         cursor.execute("""
#             SELECT id, name, mobile, email, is_active, created_at
#             FROM users
#             WHERE mobile = %s OR email = %s
#         """, (identifier, identifier))
#         user = cursor.fetchone()
#
#     if not user:
#         return {"error": "User not found"}
#     return {"user": user}
#
