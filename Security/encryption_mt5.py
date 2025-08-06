import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from database.db_connection import  get_connection
load_dotenv()

key = os.getenv("ENCRYPTION_KEY")
fernet = Fernet(key.encode())

def encrypt_password(password: str) -> str:
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password: str) -> str:
    return fernet.decrypt(encrypted_password.encode()).decode()


def get_mt5_credentials(user_id: int):
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT login, server, encrypted_password FROM mt5_credentials WHERE user_id = %s",
        (user_id,)
    )
    creds = cursor.fetchone()
    cursor.close()
    conn.close()

    if not creds:
        return None

    creds["password"] = decrypt_password(creds["encrypted_password"])
    return creds