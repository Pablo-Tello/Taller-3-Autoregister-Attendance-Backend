import jwt
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_access_token(user):
    """
    Genera un token JWT de acceso para el usuario.

    Args:
        user: Instancia del modelo User

    Returns:
        str: Token JWT codificado
    """
    payload = {
        'user_id': user.int_idUser,
        'email': user.str_email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),  # Expira en 30 minutos
        'iat': datetime.datetime.utcnow(),
        'is_docente': hasattr(user, 'docente'),
        'is_alumno': hasattr(user, 'alumno')
    }

    # Añadir el ID del docente si el usuario es un docente
    if hasattr(user, 'docente'):
        payload['docente_id'] = user.docente.str_idDocente

    # Añadir el ID del alumno si el usuario es un alumno
    if hasattr(user, 'alumno'):
        payload['alumno_id'] = user.alumno.str_idAlumno

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

def generate_refresh_token(user):
    """
    Genera un token JWT de refresco para el usuario.

    Args:
        user: Instancia del modelo User

    Returns:
        str: Token JWT de refresco codificado
    """
    payload = {
        'user_id': user.int_idUser,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),  # Expira en 7 días
        'iat': datetime.datetime.utcnow(),
        'token_type': 'refresh'
    }

    return jwt.encode(
        payload,
        settings.JWT_REFRESH_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

def decode_access_token(token):
    """
    Decodifica y valida un token JWT de acceso.

    Args:
        token: Token JWT codificado

    Returns:
        dict: Payload del token decodificado

    Raises:
        jwt.ExpiredSignatureError: Si el token ha expirado
        jwt.InvalidTokenError: Si el token es inválido
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError('Token expirado')
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError('Token inválido')

def decode_refresh_token(token):
    """
    Decodifica y valida un token JWT de refresco.

    Args:
        token: Token JWT de refresco codificado

    Returns:
        dict: Payload del token decodificado

    Raises:
        jwt.ExpiredSignatureError: Si el token ha expirado
        jwt.InvalidTokenError: Si el token es inválido
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        # Verificar que sea un token de refresco
        if payload.get('token_type') != 'refresh':
            raise jwt.InvalidTokenError('No es un token de refresco')

        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError('Token de refresco expirado')
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError('Token de refresco inválido')

def generate_qr_token(sesion_clase_id, docente_id, expiration_seconds=30):
    """
    Genera un token JWT para un código QR de asistencia.

    Args:
        sesion_clase_id: ID de la sesión de clase
        docente_id: ID del docente
        expiration_seconds: Tiempo de expiración en segundos (por defecto 30)

    Returns:
        str: Token JWT codificado
        datetime: Fecha y hora de expiración
    """
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration_seconds)

    payload = {
        'sesion_clase_id': sesion_clase_id,
        'docente_id': docente_id,
        'exp': expiration_time,
        'iat': datetime.datetime.utcnow(),
        'token_type': 'qr_code'
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token, expiration_time

def decode_qr_token(token):
    """
    Decodifica y valida un token JWT de código QR.

    Args:
        token: Token JWT codificado

    Returns:
        dict: Payload del token decodificado

    Raises:
        jwt.ExpiredSignatureError: Si el token ha expirado
        jwt.InvalidTokenError: Si el token es inválido
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        # Verificar que sea un token de código QR
        if payload.get('token_type') != 'qr_code':
            raise jwt.InvalidTokenError('No es un token de código QR')

        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError('Código QR expirado')
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError('Código QR inválido')
