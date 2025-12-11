"""
Utility functions for the whistleblower system.
"""
from cryptography.fernet import Fernet
from django.conf import settings
import base64
import hashlib


def get_encryption_key():
    """
    Generate a consistent encryption key from Django's SECRET_KEY.
    """
    # Use the first 32 bytes of the SHA256 hash of SECRET_KEY
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return base64.urlsafe_b64encode(key)


def encrypt_field(value):
    """
    Encrypt a string value.
    """
    if not value:
        return None
    
    cipher = Fernet(get_encryption_key())
    encrypted = cipher.encrypt(value.encode())
    return encrypted.decode()


def decrypt_field(encrypted_value):
    """
    Decrypt an encrypted string value.
    """
    if not encrypted_value:
        return None
    
    cipher = Fernet(get_encryption_key())
    decrypted = cipher.decrypt(encrypted_value.encode())
    return decrypted.decode()
