import uuid
import hashlib

def string_to_sha256(s: str) -> str:
   """Return the SHA-256 hex digest of the given string."""
   return hashlib.sha256(s.encode('utf-8')).hexdigest()


def generate_random_password(length=32):
    """
    生成指定长度的UUID字符串，每5个字符用下划线分隔
    
    参数:
    length: 生成的UUID字符串长度（默认32）
    
    返回:
    格式化后的UUID字符串
    """
    # 生成标准UUID并移除连字符
    full_uuid = str(uuid.uuid4()).replace('-', '')
    
    # 如果请求的长度大于标准UUID长度(32)，重复UUID直到达到所需长度
    if length > len(full_uuid):
        repeats = (length + len(full_uuid) - 1) // len(full_uuid)
        full_uuid = (full_uuid * repeats)[:length]
    else:
        full_uuid = full_uuid[:length]
    
    # 每5个字符插入一个下划线
    formatted_uuid = '_'.join([full_uuid[i:i+5] for i in range(0, len(full_uuid), 5)])
    
    return formatted_uuid
