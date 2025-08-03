from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from app.core.config import settings


class VerifyToken:
    """Does all the token verification using Auth0"""

    def __init__(self):
        self.config = settings

        # Auth0 configuration
        jwks_url = f"https://{self.config.AUTH0_DOMAIN}/.well-known/jwks.json"
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    async def verify(self, token: str):
        try:
            # Get the signing key from Auth0
            signing_key = self.jwks_client.get_signing_key_from_jwt(token).key

            # Decode and verify the token
            payload = jwt.decode(
                token,
                signing_key,
                algorithms=self.config.AUTH0_ALGORITHMS,
                audience=self.config.AUTH0_API_AUDIENCE,
                issuer=self.config.AUTH0_ISSUER,
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.JWTClaimsError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid claims",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Unable to parse authentication token: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )


token_auth_scheme = HTTPBearer()
verify_token = VerifyToken()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
):
    """Get current user from Auth0 token"""
    token = credentials.credentials
    payload = await verify_token.verify(token)

    # Extract user info from token
    user = {
        "sub": payload.get("sub"),  # Auth0 user ID
        "email": payload.get("email"),
        "name": payload.get("name"),
        "permissions": payload.get("permissions", []),
    }

    return user


# Optional: Role-based access control
def require_permission(permission: str):
    """Decorator to require specific permissions"""

    async def permission_dependency(current_user: dict = Depends(get_current_user)):
        if permission not in current_user.get("permissions", []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required",
            )
        return current_user

    return permission_dependency
