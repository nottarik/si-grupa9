import json
import logging

logger = logging.getLogger(__name__)

_fernet: object = None
_fernet_loaded = False


def _get_fernet():
    global _fernet, _fernet_loaded
    if not _fernet_loaded:
        _fernet_loaded = True
        from app.core.config import settings
        from cryptography.fernet import Fernet
        raw = settings.TOKEN_MAP_KEY.strip()
        if raw:
            _fernet = Fernet(raw.encode())
        else:
            key = Fernet.generate_key()
            logger.warning(
                "TOKEN_MAP_KEY not set; generated ephemeral key. "
                "Token maps will not survive a restart."
            )
            _fernet = Fernet(key)
    return _fernet


def encrypt_token_map(token_map: dict[str, str]) -> str:
    f = _get_fernet()
    plaintext = json.dumps(token_map, ensure_ascii=False).encode()
    return f.encrypt(plaintext).decode()


def decrypt_token_map(encrypted: str) -> dict[str, str]:
    f = _get_fernet()
    plaintext = f.decrypt(encrypted.encode())
    return json.loads(plaintext)
