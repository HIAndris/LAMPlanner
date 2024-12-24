def WorkingDir():
    import os
    import sys

    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


def SignUp(name, password) -> bool:
    inDir = WorkingDir()
    
    


def LogIn(name, password) -> bool:
    pass


def CreatePasswordHash(password: str) -> bytes:
    import hashlib
    import base64

    hash = hashlib.sha3_512(password.encode())
    base64Hash = base64.b64encode(hash.digest())
    
    return base64Hash


def CreateEncryptionKey(name: str, password: str) -> bytes:
    import hashlib
    
    hash = hashlib.sha256(password.encode()).digest()
    iv = hashlib.sha256(name.encode()).digest()
    
    key = bytearray()
    for i in range(len(hash)):
        key.append((hash[i] + iv[i]) % 256)
    
    return bytes(key)


def RotateLeft(byte: int, shift: int) -> int:
    return ((byte << shift) & 0xFF) | (byte >> (8 - shift))


def RotateRight(byte: int, shift: int) -> int:
    return ((byte >> shift) | (byte << (8 - shift))) & 0xFF


def Encrypt(data: str, key: bytes) -> bytes:
    dataBytes = bytes(data, "utf-8")
    encrypted = bytearray()
    keyLen = len(key)
    for i, byte in enumerate(dataBytes):
        shift = key[i % keyLen] % 8
        encrypted.append(RotateLeft(byte, shift))
    
    encryptedLen = len(encrypted)
    k = 0
    for _ in range(32):
        i = 0
        for i in range(encryptedLen):
            j = key[k % keyLen] % encryptedLen
            encrypted[i], encrypted[j] = encrypted[j], encrypted[i]
            k += 1
    
    return bytes(encrypted)


def Decrypt(data: bytes, key: bytes) -> str:
    keyLen = len(key)
    decryptedLen = len(data)
    
    unshuffled = bytearray(data)
    k = (32 * decryptedLen) - 1
    for _ in range(32):
        for i in range(decryptedLen - 1, -1, -1):
            j = key[k % keyLen] % decryptedLen
            unshuffled[i], unshuffled[j] = unshuffled[j], unshuffled[i]
            k -= 1
    
    decrypted = bytearray()
    for i, byte in enumerate(unshuffled):
        shift = key[i % keyLen] % 8
        decrypted.append(RotateRight(byte, shift))

    return decrypted.decode("utf-8")


def Store(name: str, key: bytes, title: str, text: str, date: str = None, status: bool = False) -> bool:
    pass


def Read(name: str, key: bytes, title: str) -> list:
    pass


def Users() -> list:
    import os
    
    inDir = WorkingDir()
    
    with open(os.path.join(inDir, "users", "users.txt"), "r", encoding="utf-8") as f:
        try:
            name, serial = f.readline().split(" ")
        except Exception as e:
            print(e)


def EditProperties(name: str, key: bytes, title: str, newTitle: str = None, newDate: str = None, newStatus: bool = None):
    pass


def UserStored(name: str, key: bytes) -> list:
    pass


def Delete(name: str, key: bytes, title: str) -> bool:
    pass