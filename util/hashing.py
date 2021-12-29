from passlib.context import CryptContext

# Hashing algorithm to use
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return password_context.hash(password)
