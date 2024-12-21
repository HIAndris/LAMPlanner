def PasswordHash(password: str):
    import hashlib
    import os
    import base64

    hash = hashlib.sha3_512(password.encode())
    base64Hash = base64.b64encode(hash.digest())
    
    return base64Hash

def SignUp(name, password):
    pass

def LogIn(name, password):
    pass

def Store(name: str, passwordHash: bytes, title: str, text: str):
    pass

def Read(name: str, passwordHash: bytes, title: str, text: str):
    pass

def Users():
    pass

def UserStored(name: str):
    pass

def Delete(name: str, passwordHash: bytes, title: str):
    pass