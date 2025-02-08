from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import credentials, auth
from requests import Session
from app.core.config import settings
from app.models.user_model import User as UserModel
from app.core.database import get_db

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
    try:
        # Verify the token with Firebase Admin SDK and allow small clock skew
        decoded_token = auth.verify_id_token(id_token, clock_skew_seconds=5)
        return decoded_token
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Firebase token has expired"
        )
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token"
        )
    except auth.RevokedIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Firebase token has been revoked"
        )
    except Exception as e:
        print(f"Error verifying Firebase token: {e}")  # Logs the exact error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token"
        )
    
def get_current_user(db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> UserModel:
    """
    Gets the current user from a Firebase ID token.a

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
    current_user : UserModel = db.query(UserModel).filter(UserModel.id == decoded_token["uid"]).first()

    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    return current_user
