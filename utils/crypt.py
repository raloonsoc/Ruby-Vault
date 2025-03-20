from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import os

class Crypt():
    def __init__(self):
        self.cipher_suite = None
        self.verifier = None
    
    def generate_master_password(self, password):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.cipher_suite = Fernet(key)
        self.verifier = self.encrypt("verification")
        return salt, self.verifier
    
    def load_key(self, password, salt, stored_verifier):
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.cipher_suite = Fernet(key)

        try:
            decrypt_stored_verifier = self.decrypt(stored_verifier)
            if decrypt_stored_verifier != "verification":
                return False
            else:
                return True
        except:
            return False
    
    def encrypt(self, plaintext):
        if self.cipher_suite is None:
            raise ValueError("Cipher suite not initialized. Generate a master password first.")
        return self.cipher_suite.encrypt(plaintext.encode()).decode()
    
    def decrypt(self, ciphertext):
        if self.cipher_suite is None:
            raise ValueError("Cipher suite not initialized. Generate a master password first.")
        return self.cipher_suite.decrypt(ciphertext.encode()).decode()
