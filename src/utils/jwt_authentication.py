from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.contrib.auth import get_user_model
from .jwt_utils import decode_access_token

User = get_user_model()

class JWTAuthentication(BaseAuthentication):
    """
    Autenticación personalizada para JWT.
    """
    
    def authenticate(self, request):
        """
        Autentica al usuario utilizando el token JWT en el encabezado Authorization.
        
        Args:
            request: Objeto request de Django
            
        Returns:
            tuple: (user, token) si la autenticación es exitosa, None en caso contrario
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Bearer '):
            return None
            
        token = auth_header.split(' ')[1]
        
        if not token:
            return None
            
        try:
            payload = decode_access_token(token)
            user_id = payload['user_id']
            
            user = User.objects.get(int_idUser=user_id)
            
            if not user.is_active:
                raise AuthenticationFailed('Usuario inactivo o eliminado')
                
            return (user, token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expirado')
        except (jwt.InvalidTokenError, User.DoesNotExist):
            raise AuthenticationFailed('Token inválido')
        except Exception as e:
            raise AuthenticationFailed(f'Error de autenticación: {str(e)}')
