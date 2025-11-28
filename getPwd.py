import secrets
import string
import hashlib

def generate_random_password(length=12):
   alphabet = string.ascii_letters + string.digits + string.punctuation
   password = ''.join(secrets.choice(alphabet) for _ in range(length))
   return password

def string_to_sha256(s: str) -> str:
   """Return the SHA-256 hex digest of the given string."""
   return hashlib.sha256(s.encode('utf-8')).hexdigest()

