def string_to_sha256(s: str) -> str:
   """Return the SHA-256 hex digest of the given string."""
   return hashlib.sha256(s.encode('utf-8')).hexdigest()


import uuid
import hashlib
import secrets
import string

def generate_random_password(length=16):
    """基于UUID生成高强度密码"""
    # 生成UUID
    raw_uuid = uuid.uuid4()
    
    # 将UUID转换为哈希值
    hash_obj = hashlib.sha256(str(raw_uuid).encode())
    hash_hex = hash_obj.hexdigest()
    
    # 定义字符集
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
    
    # 从哈希值生成密码
    password = []
    for i in range(length):
        # 使用哈希值作为随机源
        index = int(hash_hex[i*2:i*2+2], 16) % len(all_chars)
        password.append(all_chars[index])
    
    return ''.join(password)
