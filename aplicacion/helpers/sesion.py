"""
Modulo sesion
"""
import hashlib
import json
import uuid
from datetime import timedelta
from typing import TYPE_CHECKING
from typing import Dict
from typing import Optional

import jwt

if TYPE_CHECKING:
    from redis import Redis

# from aplicacion.helpers.utilidades import Utilidades


class Sesion():
    """
    Contiene los manejos de token generacion de hash y codificacion del jwt
    """

    def generar_token(
        self,
        redis: 'Redis',
        secret_key: str,
        lifetime_jwt: timedelta,
        user_id: int,
        data: Dict
    ):
        """
        Genera el token de acceso y lo guarda en el redis
        """
        try:
            encoded = jwt.encode(data, secret_key, algorithm='HS256')
            data['user_id'] = user_id
            redis.setex(f'jwt-{encoded}', lifetime_jwt, json.dumps(data))
            return encoded
        except Exception:
            return None

    def eliminar_token(self, redis: 'Redis', jwt_token: str):
        """
        Elimina el token del redis
        """
        try:
            return redis.delete(f'jwt-{jwt_token}')
        except Exception:
            return None

    def validar_token(self, redis, jwt_token):
        """
        revisa si existe el jwt en el redis
        """
        return redis.exists(f'jwt-{jwt_token}')

    def generate_hash(self, password: str, salt: Optional[str] = None):
        """
        genera el hash de seguridad con m5 y sha 256
        """
        salt = salt or str(uuid.uuid1())
        hash_final = hashlib.sha256(
            hashlib.md5(
                (salt + password).encode()
            ).hexdigest().encode()
        ).hexdigest()
        return (salt, hash_final)

    def decode_jwt(self, jwt_token: str, secret_key: str):
        """
        Decodifica el jwt para ver la información
        """
        return jwt.decode(jwt_token, secret_key, algorithms=['HS256', ])
