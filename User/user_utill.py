import hashlib
import datetime
import random
import re
import requests

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def create_user(db, name, mobile, email, password):
    password_hash = hash_password(password)

    with db.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT id FROM users WHERE mobile = %s OR email = %s", (mobile, email))
        if cursor.fetchone():
            return False, "Mobile or Email already registered"

        cursor.execute("""
            INSERT INTO users (name, mobile, email, password, is_active)
            VALUES (%s, %s, %s, %s, 1)
        """, (name, mobile, email, password_hash))
    db.commit()
    return True, "User created successfully"

def login_user(db, identifier, password):
    with db.cursor(dictionary=True) as cursor:
        if '@' in identifier:
            cursor.execute("SELECT * FROM users WHERE email = %s", (identifier,))
        else:
            cursor.execute("SELECT * FROM users WHERE mobile = %s", (identifier,))
        user = cursor.fetchone()

        if not user:
            return False, "User not found"

        if not user["is_active"]:
            return False, "User is not active"

        if user["password"] != hash_password(password):
            return False, "Incorrect password"

    return True, {
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "mobile": user["mobile"],
            "email": user["email"],
            "created_at": user["created_at"]
        }
    }

def get_user_by_identifier(db, identifier):
    with db.cursor(dictionary=True) as cursor:
        if identifier.isdigit():
            cursor.execute("SELECT * FROM users WHERE mobile = %s", (identifier,))
        else:
            cursor.execute("SELECT * FROM users WHERE email = %s", (identifier,))
        return cursor.fetchone()

# ===========================================use when sms provider available ================================

# def is_valid_mobile(mobile):
#     return bool(re.fullmatch(r"[6-9]\d{9}", mobile))
#
# def send_sms_otp(mobile: str, otp: str):
#     url = "https://www.fast2sms.com/dev/bulkV2"
#     headers = {
#         'authorization': "YOUR_FAST2SMS_API_KEY",  # Replace with real API key
#         'Content-Type': "application/x-www-form-urlencoded"
#     }
#     payload = {
#         'variables_values': otp,
#         'route': 'otp',
#         'numbers': mobile
#     }
#     response = requests.post(url, data=payload, headers=headers)
#     return response.status_code == 200
#
#
# def send_password_change_otp_service(db, identifier):
#     if identifier.isdigit() and not is_valid_mobile(identifier):
#         return False, "Invalid mobile number"
#
#     user = get_user_by_identifier(db, identifier)
#     if not user:
#         return False, "User not found"
#
#     otp = generate_otp()
#     otp_expiry = datetime.datetime.now() + datetime.timedelta(minutes=5)
#
#     with db.cursor(dictionary=True) as cursor:
#         cursor.execute("DELETE FROM pending_users WHERE mobile = %s", (user["mobile"],))
#         cursor.execute("""
#             INSERT INTO pending_users (name, mobile, password_hash, otp_code, otp_expires_at)
#             VALUES (%s, %s, %s, %s, %s)
#         """, (user["name"], user["mobile"], user["password"], otp, otp_expiry))
#     db.commit()
#
#     if send_sms_otp(user["mobile"], otp):
#         return True, "OTP sent to mobile"
#     else:
#         return False, "Failed to send OTP"
#
# def verify_password_change_otp_and_update(db, mobile, otp_code, new_password):
#     with db.cursor(dictionary=True) as cursor:
#         cursor.execute("SELECT * FROM pending_users WHERE mobile = %s", (mobile,))
#         row = cursor.fetchone()
#         if not row:
#             return False, "No pending OTP found"
#
#         if row["otp_code"] != otp_code:
#             return False, "Incorrect OTP"
#         if datetime.datetime.now() > row["otp_expires_at"]:
#             return False, "OTP expired"
#
#         new_hash = hash_password(new_password)
#         cursor.execute("UPDATE users SET password = %s WHERE mobile = %s", (new_hash, mobile))
#         cursor.execute("DELETE FROM pending_users WHERE mobile = %s", (mobile,))
#     db.commit()
#     return True, "Password updated successfully"

# ===========================================use when sms provider available ^^^^^   ================================

# ============================================remove it wehn sms provider===========================================================

def send_password_change_otp(db, identifier):
    user = get_user_by_identifier(db, identifier)
    if not user:
        return False, "User not found"

    otp = generate_otp()
    otp_expiry = datetime.datetime.now() + datetime.timedelta(minutes=5)

    with db.cursor(dictionary=True) as cursor:
        cursor.execute("DELETE FROM pending_users WHERE mobile = %s", (user["mobile"],))
        cursor.execute("""
            INSERT INTO pending_users (name, mobile, password_hash, otp_code, otp_expires_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (user["name"], user["mobile"], user["password"], otp, otp_expiry))
    db.commit()
    return True, otp




def change_password_by_otp(db, mobile, otp_code, new_password):
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM pending_users WHERE mobile = %s", (mobile,))
        row = cursor.fetchone()
        if not row:
            return False, "No pending OTP found"

        if row["otp_code"] != otp_code or datetime.datetime.now() > row["otp_expires_at"]:
            return False, "Invalid or expired OTP"

        new_hash = hash_password(new_password)
        cursor.execute("UPDATE users SET password = %s WHERE mobile = %s", (new_hash, mobile))
        cursor.execute("DELETE FROM pending_users WHERE mobile = %s", (mobile,))
    db.commit()
    return True, "Password updated successfully"

# ============================================remove it wehn sms provider^^^===========================================================

def update_password_by_old_password(db, identifier, old_password, new_password):
    user = get_user_by_identifier(db, identifier)
    if not user:
        return False, "User not found"

    if user["password"] != hash_password(old_password):
        return False, "Incorrect current password"

    new_hash = hash_password(new_password)
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_hash, user["id"]))
    db.commit()
    return True, "Password updated successfully"


def update_user_info_by_identifier(db, identifier, password, new_name=None, new_mobile=None, new_email=None):
    user = get_user_by_identifier(db, identifier)
    if not user:
        return False, "User not found"

    if user["password"] != hash_password(password):
        return False, "Incorrect password"

    updated_name = new_name or user["name"]
    updated_mobile = new_mobile or user["mobile"]
    updated_email = new_email or user["email"]
    with db.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT id FROM users WHERE mobile = %s AND id != %s", (updated_mobile, user["id"]))
        if cursor.fetchone():
            return False, "Check Your Mobile Number"

        cursor.execute("SELECT id FROM users WHERE email = %s AND id != %s", (updated_email, user["id"]))
        if cursor.fetchone():
            return False, "Check Your Email"

        cursor.execute("""
            UPDATE users
            SET name = %s, mobile = %s, email = %s
            WHERE id = %s
        """, (updated_name, updated_mobile, updated_email, user["id"]))

    db.commit()

    return True, {
        "message": "User info updated",
        "user": {
            "id": user["id"],
            "name": updated_name,
            "mobile": updated_mobile,
            "email": updated_email,
            "created_at": user["created_at"]
        }
    }

def delete_user_by_identifier(db, identifier, password):
    user = get_user_by_identifier(db, identifier)
    if not user:
        return False, "User not found"

    if user["password"] != hash_password(password):
        return False, "Incorrect password"

    with db.cursor(dictionary=True) as cursor:
        cursor.execute("DELETE FROM users WHERE id = %s", (user["id"],))
    db.commit()
    return True, "User deleted successfully"