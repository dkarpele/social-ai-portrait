"""
This module provides helper functions for digital signature verification using RSA.

It offers functionalities for:

- Generating a digital signature for a message using a private key.
- Retrieving the public key from a stored file.
- Verifying the authenticity of a message using a signature and a public key.
"""

import logging
import os
import rsa
from rsa.pkcs1 import VerificationError

logger = logging.getLogger(__name__)


def get_signature(message: bytes, hash_method: str = 'MD5') -> bytes:
    """
    Generates a digital signature for the provided message using a private key.

    This function retrieves the private key from a file specified by the
    `PRIVATE_KEY_FILEPATH` environment variable and uses it to sign the
    given message with the specified hash method (defaults to MD5).

    :param message: The message bytes to be signed.
    :param hash_method: The hashing algorithm to use (default: 'MD5').
    :return: The digital signature of the message as bytes.
    """
    logger.info('Trying to get signature.')
    with open(os.getenv('PRIVATE_KEY_FILEPATH'), 'rb') as private_file:
        private_key_data = private_file.read()
    private_key = rsa.PrivateKey.load_pkcs1(private_key_data, 'PEM')

    return rsa.sign(message, private_key, hash_method)


def get_public_key():
    """
    Retrieves the public key from a stored file.

    This function reads the public key from a file specified by the
    `PUBLIC_KEY_FILEPATH` environment variable.

    :return: The public key object loaded from the file.
    """
    logger.info('Trying to get public key.')
    with open(os.getenv('PUBLIC_KEY_FILEPATH'), 'rb') as public_file:
        public_key_data = public_file.read()

    return rsa.PublicKey.load_pkcs1(public_key_data)


def verify_message(message: bytes, signature: bytes, public_key) -> bool | str:
    """
    Verifies the authenticity of a message using a digital signature and a
    public key.

    This function attempts to verify the signature of the provided message
    using the given public key. It logs a warning if the signature is empty
    or verification fails.

    :param message: The message bytes to be verified.
    :param signature: The digital signature of the message as bytes.
    :param public_key: The public key object used for verification.
    :return: True if the message signature is valid, False otherwise.
    """
    if not signature:
        logger.warning('Signature is empty. User probably does something '
                       'dangerous.')
        return False
    try:
        return rsa.verify(message, signature, public_key)
    except VerificationError:
        logger.warning("Verification failed")
