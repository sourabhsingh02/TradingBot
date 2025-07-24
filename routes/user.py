from fastapi import APIRouter, Depends, HTTPException
from database.db_connection import get_connection
from User.user_utill import *
from database.users_schema import *

router = APIRouter(prefix="/user", tags=["User"])


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

    return {
        "status": "success",
        "message": result["message"],
        "user": result["user"]
    }

# 3. Update User Info API
@router.post("/update-user-info")
def update_user_info(payload: UpdateUserInfoRequest, db=Depends(get_connection)):
    success, result = update_user_info_by_identifier(
        db,
        identifier=payload.identifier,
        password=payload.password,
        new_name=payload.new_name,
        new_mobile=payload.new_mobile,
        new_email=payload.new_email
    )
    if success:
        return {"success": True, **result}
    return {"success": False, "error": result}


@router.post("/update-password")
def update_password(payload: UpdatePasswordRequest, db=Depends(get_connection)):
    success, message = update_password_by_old_password(
        db,
        identifier=payload.identifier,
        old_password=payload.old_password,
        new_password=payload.new_password
    )
    if success:
        return {"success": True, "message": message}
    return {"success": False, "error": message}

# ===========================================use when sms provider available ================================


# @router.post("/send-password-change-otp-service")
# def send_password_change_otp_api(payload: IdentifierRequest, db=Depends(get_connection)):
#     success, message = send_password_change_otp_service(db, payload.identifier)
#     if success:
#         return {"success": True, "message": message}
#     return {"success": False, "error": message}
#
#
# @router.post("/verify-password-change-otp")
# def verify_password_change_otp_api(payload: PasswordChangeByOtpRequest, db=Depends(get_connection)):
#     success, message = verify_password_change_otp_and_update(
#         db, payload.mobile, payload.otp_code, payload.new_password
#     )
#     if success:
#         return {"success": True, "message": message}
#     return {"success": False, "error": message}

# ===========================================use when sms provider available ^^^================================

# ============================================remove it wehn sms provider===========================================================
@router.post("/send-password-change-otp")
def send_otp(payload: IdentifierRequest, db=Depends(get_connection)):
    success, otp_or_msg = send_password_change_otp(db, payload.identifier)
    if success:
        return {"success": True, "otp": otp_or_msg}  # Only show OTP in dev/testing
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

# ============================================remove it wehn sms provider ^^ ===========================================================



@router.delete("/delete")
def delete_user(payload: DeleteUserRequest, db=Depends(get_connection)):
    success, msg = delete_user_by_identifier(db, payload.identifier, payload.password)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}


@router.get("/all-users", summary="Get all users (with password)")
def get_all_users(db=Depends(get_connection)):
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    return {"users": users}


@router.get("/users-by-identifier/{identifier}", summary="Get user by identifier (mobile or email), without password")
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

# from fastapi import APIRouter, Depends, HTTPException ,Query
# from database.db_connection import get_connection
# from User.user_utill import *
# from database.users_schema import *
# router = APIRouter(prefix="/user", tags=["User"])
#
# @router.post("/signup")
# def signup(name: str, mobile: str, email: str, password: str, db=Depends(get_connection)):
#     otp = create_pending_user(db, name, mobile, email, password)
#     return {"message": "OTP sent", "otp_for_testing": otp}
#
# @router.post("/verify-signup")
# def verify_signup(mobile: str, otp_code: str, email: str, db=Depends(get_connection)):
#     success, msg = verify_signup_otp(db, mobile, otp_code, email)
#     if not success:
#         raise HTTPException(status_code=400, detail=msg)
#     return {"message": msg}
#
#
#
#
#
# @router.post("/login")
# def login(mobile: str = None, email: str = None, password: str = "", db=Depends(get_connection)):
#     identifier = mobile or email
#
#     if not identifier:
#         raise HTTPException(status_code=400, detail="Provide either mobile or email")
#
#     if not password:
#         raise HTTPException(status_code=400, detail="Password is required")
#
#     success, result = login_user(db, identifier=identifier, password=password)
#
#     if not success:
#         raise HTTPException(status_code=401, detail=result)
#
#     return {
#         "status": "success",
#         "message": result["message"],
#         "user": result["user"]
#     }
#
#
# @router.get("/get_all")
# def get_all_users(db=Depends(get_connection)):
#     return get_all_users(db)
#
# @router.post("/get_byidentifier")
# def get_user(user: UserBase, db=Depends(get_connection)):
#     result = get_user_by_mobile_or_email(db, user.mobile, user.email)
#     if not result:
#         raise HTTPException(status_code=404, detail="User not found")
#     return result
#
#
#
#
# @router.post("/change-password")
# def change_password(
#     identifier: str = Query(..., description="Mobile or Email"),
#     old_password: str = Query(...),
#     new_password: str = Query(...),
#     db=Depends(get_connection)
# ):
#     success, result = change_user_password(db, identifier, old_password, new_password)
#     if success:
#         return {"success": True, "message": result}
#     return {"success": False, "error": result}
#
#
#
# @router.post("/update-user-info")
# def update_user_info(
#     identifier: str = Query(...),
#     password: str = Query(...),
#     new_name: str = Query(None),
#     new_mobile: str = Query(None),
#     new_email: str = Query(None),
#     db=Depends(get_connection)
# ):
#     success, result = update_user_info(db, identifier, password, new_name, new_mobile, new_email)
#     if success:
#         return {"success": True, **result}
#     return {"success": False, "error": result}
#
#
# @router.delete("/delete")
# def delete_user(
#     mobile: str = Query(None),
#     email: str = Query(None),
#     password: str = Query(...),
#     db=Depends(get_connection)
# ):
#     success, msg = delete_user(db, mobile, email, password)
#     if not success:
#         raise HTTPException(status_code=400, detail=msg)
#     return {"message": msg}
#
