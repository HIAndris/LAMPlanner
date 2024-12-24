def WorkingDir():
    import os
    import sys

    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def SignUp(name: str, password: str) -> bool:
    """Adds a user to the user database and creates a dictionary for them

    Args:
        name (str): the chosen username
        password (str): the chosen password

    Returns:
        bool: Returns True if the user has been created and returns False and a description if there was a problem during the creation.
    """
    import os
    
    inDir = WorkingDir()
    
    if name in Users():
        return False, "This username already exists!"
    
    if "\n" in name:
        return False, "The name has newline character(s) in it!"
    
    passwordHash = CreatePasswordHash(password)
    users = Users("s")
    if len(users) == 0:
        serial = 0
    else:
        serial = max(users) + 1
    
    with open(os.path.join(inDir, "users", "users.txt"), "a", encoding="utf-8") as f:
        f.write(name + " " + str(serial) + " " + passwordHash + "\n")
    
    os.makedirs(os.path.dirname(inDir, "users", str(serial)), exist_ok = True)
    with open(os.path.join(inDir, "users", str(serial), "user.hiasecret"), "", encoding="utf-8") as f:
        pass
    
    return True


def LogIn(name: str, password: str) -> bool:
    pass


def CreatePasswordHash(password: str) -> str:
    """Creates the password hash used to validate a password.

    Args:
        password (str): user's password

    Returns:
        str: the password hash in str
    """
    import hashlib
    import base64

    hash = hashlib.sha3_512(password.encode())
    base64Hash = base64.b64encode(hash.digest())
    
    return base64Hash.decode("utf-8")


def CreateEncryptionKey(name: str, password: str) -> bytes:
    """Creates the encryption key used for storing data.

    Args:
        name (str): username
        password (str): the user's password

    Returns:
        bytes: the encryption key
    """
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


def Store(id: str, key: bytes, title: str, text: str, date: str = None, status: bool = False) -> bool:
    pass


def Read(id: str, key: bytes, title: str) -> list:
    pass


def Users(mode: str = "u") -> list:
    """Returns the users stored in the program.

    Args:
        mode (str, optional): The mode sets the type of information returned back: "u"= usernames, "f"= usernames, serial numbers and password hashes, "s"= serial numbers, "v"=usernames and password hashes. Defaults to "u".

    Raises:
        SyntaxError: Invalid mode is given.
        SyntaxError: The users.txt has incorrect syntax.

    Returns:
        list: List of users.
    """
    import os
    
    if mode not in ("u", "f", "s", "v"):
        raise SyntaxError("Invalid mode for filemanager.Users()!")
    users = []
    inDir = WorkingDir()
    
    with open(os.path.join(inDir, "users", "users.txt"), "r", encoding="utf-8") as f:
        reading = True
        while reading:
            line = f.readline()
            if line == "":
                reading = False
                
            else:
                try:
                    name, serial, passwordHash = line.strip().rsplit(" ", 2)
                except Exception as e:
                    raise SyntaxError("The users.txt was modified and one of the lines has incorrect syntax!")

                if mode == "u": users.append(name)
                elif mode == "f": users.append((name, int(serial), passwordHash))
                elif mode == "s": users.append(int(serial))
                else: users.append((name, passwordHash))
                
    return users


def EditProperties(id: str, key: bytes, title: str, newTitle: str = None, newDate: str = None, newStatus: bool = None):
    pass


def UserStored(id: str, key: bytes) -> list:
    pass


def Delete(id: str, key: bytes, title: str) -> bool:
    pass