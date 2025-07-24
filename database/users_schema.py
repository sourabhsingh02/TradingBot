# database/schemas/user_schemas.py

from pydantic import BaseModel , EmailStr
from typing import Optional

class SignupRequest(BaseModel):
    name: str
    mobile: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    identifier: str  # mobile or email
    password: str

class ChangePasswordRequest(BaseModel):
    identifier: str
    old_password: str
    new_password: str

class UpdateUserInfoRequest(BaseModel):
    identifier: str
    password: str
    new_name: Optional[str] = None
    new_mobile: Optional[str] = None
    new_email: Optional[EmailStr] = None

class VerifyPasswordChangeRequest(BaseModel):
    mobile: str
    otp_code: str
    new_password: str

class DeleteUserRequest(BaseModel):
    identifier: str
    password: str

class UpdatePasswordRequest(BaseModel):
    identifier: str
    old_password: str
    new_password: str

class IdentifierRequest(BaseModel):
    identifier: str

class ChangePasswordByOTPRequest(BaseModel):
    mobile: str
    otp_code: str
    new_password: str

#   use when service propvider aval
class PasswordChangeByOtpRequest(BaseModel):
        mobile: str
        otp_code: str
        new_password: str