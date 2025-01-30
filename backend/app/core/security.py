from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    Verifies a password against a given hashed password.

    Args:
        plain_password (str): The password to check.
        hashed_password (str): The hashed password to check against.

    Returns:
        bool: Whether the password matches the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Hashes a password using the default hashing algorithm.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    
    return pwd_context.hash(password)