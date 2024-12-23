def SignUp(name, password):
    pass

def LogIn(name, password):
    pass

def CreatePasswordHash(password: str):
    import hashlib
    import base64

    hash = hashlib.sha3_512(password.encode())
    base64Hash = base64.b64encode(hash.digest())
    
    return base64Hash

def CreateEncryptionKey(name: str, password: str):
    import hashlib
    import base64
    
    hash = hashlib.sha256(password.encode()).digest()
    iv = hashlib.sha256(name.encode()).digest()
    
    key = bytearray()
    for i in range(len(hash)):
        key.append((hash[i] + iv[i]) % 256)
    
    return bytes(key)

def rotate_left(byte, shift):
    return ((byte << shift) & 0xFF) | (byte >> (8 - shift))

def rotate_right(byte, shift):
    return ((byte >> shift) | (byte << (8 - shift))) & 0xFF

def Store(name: str, key: bytes, title: str, text: str):
    pass

def Read(name: str, key: bytes, title: str, text: str):
    pass

def Users():
    pass

def UserStored(name: str, key: bytes):
    pass

def Delete(name: str, key: bytes, title: str):
    pass

print(CreateEncryptionKey("józsi2", "jelszóóó00123400"))