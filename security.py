# security.py
from passlib.context import CryptContext

# Use Argon2 for hashing
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)

def get_password_hash(password: str) -> str:
    """Hashes the password using Argon2."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed one."""
    return pwd_context.verify(plain_password, hashed_password)
