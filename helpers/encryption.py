import logging
import os
import rsa
from rsa.pkcs1 import VerificationError

logger = logging.getLogger(__name__)


def get_signature(message: bytes, hash_method: str = 'MD5') -> bytes:
    logger.info('Trying to get signature.')
    with open(os.getenv('PRIVATE_KEY_FILEPATH'), 'rb') as private_file:
        private_key_data = private_file.read()
    private_key = rsa.PrivateKey.load_pkcs1(private_key_data, 'PEM')

    return rsa.sign(message, private_key, hash_method)


def get_public_key():
    logger.info('Trying to get public key.')
    with open(os.getenv('PUBLIC_KEY_FILEPATH'), 'rb') as public_file:
        public_key_data = public_file.read()

    return rsa.PublicKey.load_pkcs1(public_key_data)


def verify_message(message: bytes, signature: bytes, public_key):
    if not signature:
        logger.warning('Signature is empty. User probably does something '
                       'dangerous.')
        return False
    try:
        return rsa.verify(message, signature, public_key)
    except VerificationError:
        logger.warning("Verification failed")
