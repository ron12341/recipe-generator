from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import credentials, auth
from app.core.config import settings

# Initialize Firebase credentials
cred = credentials.Certificate(settings.FIREBASE_KEY_PATH)

# Initialize FIrebase Admin SDK
firebase_admin.initialize_app(cred)

def verify_firebase_token(id_token: str) -> dict:
    """
    Verifies a Firebase ID token using the Firebase Admin SDK.

    Args:
        id_token (str): The encoded Firebase ID token to verify.

    Returns:
        dict: The decoded claims of the ID token if verification is successful.

    Raises:
        HTTPException: If the token is invalid, an HTTP 401 Unauthorized exception is raised.
    """

    print("FIREBASE_KEY_PATH", settings.FIREBASE_KEY_PATH)
    try:
        # Verify the token with Firebase Admin SDKa
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token"
        )
    
def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> dict:
    """
    Gets the current user from a Firebase ID token.

    Args:
        authorization (HTTPAuthorizationCredentials): The Firebase ID token
            obtained from the Authorization header.

    Returns:
        dict: The decoded claims of the ID token.

    Raises:
        HTTPException: If the token is invalid, an HTTP 401 Unauthorized exception is raised.
    """
    token = authorization.credentials
    decoded_token = verify_firebase_token(token)
    return decoded_token