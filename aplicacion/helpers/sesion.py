"""
a
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
    a
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
        a
        """
        try:
            encoded = jwt.encode(data, secret_key, algorithm='HS256')
            data['jwt'] = encoded
            redis.setex(f'jwt-{user_id}', lifetime_jwt, json.dumps(data))
            return encoded
        except Exception:
            return None

    def eliminar_token(self, redis: 'Redis', user_id: int):
        """
        a
        """
        try:
            return redis.delete(f'jwt-{user_id}')
        except Exception:
            return None

    def validar_token(self, redis, user_id):
        """
        a
        """
        return redis.exists(f'jwt-{user_id}')

    def generate_hash(self, password: str, salt: Optional[str] = None):
        """
        a
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
        a
        """
        return jwt.decode(jwt_token, secret_key, algorithms=['HS256', ])
