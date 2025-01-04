def WorkingDir():
    import os
    import sys

    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def SignUp(name: str, password: str) -> bool:
    """Adds a user to the user database and creates a dictionary for them.

    Args:
        name (str): username
        password (str): password

    Returns:
        bool: Returns True if the user has been created and returns False if there was a problem during the creation.
    """
    import os
    
    inDir = WorkingDir()
    
    if name in Users():
        return False
    
    if "\n" in name:
        raise ValueError("Newline character found in username!")
    
    passwordHash = CreatePasswordHash(password)
    users = Users("s")
    if len(users) == 0:
        serial = 0
    else:
        serial = max(users) + 1
    
    with open(os.path.join(inDir, "users", "users.txt"), "a", encoding="utf-8") as f:
        f.write(name + " " + str(serial) + " " + passwordHash + "\n")
    
    os.makedirs(os.path.join(inDir, "users", str(serial)), exist_ok = True)
    with open(os.path.join(inDir, "users", str(serial), "user.info"), "w", encoding="utf-8") as f:
        pass
    
    return True


def LogIn(name: str, password: str) -> bool:
    """Validates a user by checking their username and password.

    Args:
        name (str): username
        password (str): password

    Returns:
        bool: Returns True if the user's username and password are correct and returns False if there is something wrong with the given arguments.
    """
    
    if name not in Users():
        return False
    
    if (name, CreatePasswordHash(password)) not in Users("v"):
        return False
    
    return True


def DeleteUser(name: str, password: str):
    if LogIn(name, password) == False:
        return False
    
    import os
    import shutil
    
    inDir = WorkingDir()
    with open(os.path.join(inDir, "users", "users.txt"), "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    linesLen = len(lines)
    i = 0
    line = lines[i].rsplit(" ", 2)
    while i <= linesLen and line[0] != name:
        i += 1
        line = lines[i]
    
    if linesLen < i:
        raise RuntimeError("Ez vagy bugos, vagy valaki/valami a másodperc töredéke alatt módosított egy fájlt, vagy nem tudom... :3")
    
    lines.pop(i)
    
    with open(os.path.join(inDir, "users", "users.txt"), "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line)
    
    shutil.rmtree(os.path.join(inDir, "users", line[1]))
    
    return True


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


def Users(mode: str = "u") -> list:
    """Returns the users stored in the program.

    Args:
        mode (str, optional): The mode sets the type of information returned back: "u"= usernames, "f"= usernames, serial numbers and password hashes, "s"= serial numbers, "i"= usernames and serial numbers, "v"= usernames and password hashes. Defaults to "u".

    Raises:
        SyntaxError: Invalid mode is given.
        SyntaxError: The users.txt has incorrect syntax.

    Returns:
        list: List of users.
    """
    import os
    
    if mode not in ("u", "f", "s", "i", "v"):
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
                elif mode == "i": users.append((name, int(serial)))
                else: users.append((name, passwordHash))
                
    return users


def GetUserSerial(name: str) -> int:
    users = Users("i")
    usersLen = len(users)
    if usersLen == 0:
        raise ValueError("User not found!")

    i = 0
    while i < usersLen and users[i][0] != name:
        i += 1
    
    if len(users) == i:
        raise ValueError("User not found!")
    
    return int(users[i][1])


def GetUserName(serial: int) -> str:
    users = Users("i")
    usersLen = len(users)
    if usersLen == 0:
        raise ValueError("User not found!")
    
    i = 1
    while i < usersLen and users[i][1] != serial:
        i += 1
    
    if len(users) == i:
        raise ValueError("User not found!")
    
    return users[i][0]


def StrToBool(str: str) -> bool:
    if str == "True":
        return True
    else:
        return False
    

def GetUserStored(serial: int, key: bytes, mode: str = "t") -> list:
    """Reads and returns a user's posts and post details.

    Args:
        serial (int): The user's serial number.
        key (bytes): The user's encryption key.
        mode (str, optional): Modifies the information returned. Modes: "t"= titles, "s"= post serial numbers, "ts"= titles and post serial numbers, "l"= all informations in each of the lines (titles, post serial numbers, dates and statuses), "lr"= all informations in each of the lines (titles, post serial numbers in str, dates and statuses), "p"= titles, dates, statuses, "a"= the decrypted user.info file in a single string. Defaults to "t".

    Raises:
        FileNotFoundError: In case of unexisting user.

    Returns:
        list: The list of lines in the user.info file decrypted with the amount of details chosen by the mode.
    """
    import os
    
    inDir = WorkingDir()
    serialStr = str(serial)

    if serialStr not in os.listdir(os.path.join(inDir, "users")):
        raise FileNotFoundError("The given user's folder doesn't exist!")
    
    if "user.info" in os.listdir(os.path.join(inDir, "users", serialStr)):
        with open(os.path.join(inDir, "users", str(serial), "user.info"), "rb") as f:
            userTXT = Decrypt(f.read(), key)
    else:
        userTXT = ""
    
    lines = userTXT.split("\n")
    if lines[-1] == "":
        lines.pop(-1)
    
    for i in range(len(lines)):
        lines[i] = lines[i].strip().rsplit(" ", 3)

    returnLines = []
    if mode == "t":
        for line in lines:
            returnLines.append(line[0])
    elif mode == "s":
        for line in lines:
            returnLines.append(int(line[1]))
    elif mode == "ts":
        for line in lines:
            returnLines.append((line[0], int(line[1])))
    elif mode == "l":
        for line in lines:
            returnLines.append((line[0], int(line[1]), line[2], StrToBool(line[3])))
    elif mode == "p":
        for line in lines:
            returnLines.append((line[0], line[2], StrToBool(line[3])))
    elif mode == "pl":
        for line in lines:
            returnLines.append([line[0], line[2], StrToBool(line[3])])
    elif mode == "lr":
        for line in lines:
            returnLines.append((line[0], line[1], line[2], line[3]))
    elif mode == "a":
        returnLines = userTXT
    
    return returnLines


def Store(serial: int, key: bytes, title: str, text: str, date: str, status: bool = False) -> bool:
    """Stores a new post.

    Args:
        serial (int): The user's serial number.
        key (bytes): The user's encryption key.
        title (str): The title of the post.
        text (str): The text in the post.
        date (str): A date to the post.
        status (bool, optional): The status of the post. Defaults to False.

    Returns:
        bool: True if the creation of the post was successful, False if not.
    """
    import os
    
    inDir = WorkingDir()
    serialStr = str(serial)
    
    try:
        userTXT = GetUserStored(serial, key, "a")
        
    except:
        return False
    
    if "\n" in title:
        return False
    
    userStored = GetUserStored(serial, key, "s")

    if 0 < len(userStored):
        postSerial = max(userStored) + 1
    else:
        postSerial = 0
    
    postSerial = str(postSerial)

    newUserTXT = userTXT + title + " " + postSerial + " " + date + " " + str(status) + "\n"
    with open(os.path.join(inDir, "users", serialStr, "user.info"), "wb") as f:
        f.write(Encrypt(newUserTXT, key))
    
    with open(os.path.join(inDir, "users", serialStr, postSerial + ".post"), "wb") as f:
        f.write(Encrypt(text, key))
        
    return True


def Read(serial: int, key: bytes, title: str) -> dict:
    """Reads and returns a post.

    Args:
        serial (int): The user's serial number.
        key (bytes): The user's encryption key.
        title (str): The title of the post.

    Returns:
        dict: The dictionary with the post's details and text, returns an empty dictionary if the post was not found or if the user doesn't exist.
    """
    import os
    
    inDir = WorkingDir()
    serialStr = str(serial)
    
    try:
        userTXT = GetUserStored(serial, key, "l")
        
    except:
        return {}
    
    if 0 == len(userTXT):
        return {}
    
    userTXTLen = len(userTXT)
    line = userTXT[0]
    index = 1
    while index < userTXTLen and line[0] != title:
        line = userTXT[index]
        index += 1
    
    if userTXTLen < index:
        return {}
    
    with open(os.path.join(inDir, "users", serialStr, str(line[1])) + ".post", "rb") as f:
        text = Decrypt(f.read(), key)

    return {"title": line[0], "date": line[2], "status": line[3], "text": text}
    

def EditProperties(serial: int, key: bytes, title: str, newTitle: str = None, newDate: str = None, newStatus: bool = None) -> bool:
    """Edits the details of a post.

    Args:
        serial (int): The user's serial number.
        key (bytes): The user's encryption key.
        title (str): The title of the post.
        newTitle (str, optional): The new title for the post. Defaults to None.
        newDate (str, optional): The new date for the post. Defaults to None.
        newStatus (bool, optional): The new status for the post. Defaults to None.

    Returns:
        bool: True if the post's details has been successfully changed to the new ones, False if not.
    """
    import os
    
    inDir = WorkingDir()
    serialStr = str(serial)
    
    try:
        userTXT = GetUserStored(serial, key, "lr")
        
    except:
        return False
    
    if 0 == len(userTXT):
        return False
    
    userTXTLen = len(userTXT)
    line = userTXT[0]
    index = 1
    while index < userTXTLen and line[0] != title:
        line = userTXT[index]
        index += 1
    
    if userTXTLen < index:
        return False
    
    if isinstance(newTitle, str) and "\n" in newTitle:
        return False
    
    if newTitle == None:
        newTitle = line[0]
    
    if newDate == None:
        newDate = line[2]
        
    if newStatus == None:
        newStatus = line[3]
    
    userTXT[index - 1] = (newTitle, line[1], newDate, str(newStatus))
    
    for i in range(len(userTXT)):
        userTXT[i] = " ".join(userTXT[i]) + "\n"
    
    userTXT = "".join(userTXT)
    
    with open(os.path.join(inDir, "users", serialStr, "user.info"), "wb") as f:
        f.write(Encrypt(userTXT, key))

    return True


def EditText(serial: int, key: bytes, title: str, newText: str) -> bool:
    """Edits the text of a post.

    Args:
        serial (int): The user's serial number.
        key (bytes): The user's encryption key.
        title (str): The title of the post.
        newText (str): The new text for the post.

    Returns:
        bool: True if the post's text has been successfully changed to the new text, False if not.
    """
    import os
    
    inDir = WorkingDir()
    serialStr = str(serial)
    
    try:
        userTXT = GetUserStored(serial, key, "ts")
        
    except:
        return False
    
    if 0 == len(userTXT):
        return False
    
    userTXTLen = len(userTXT)
    line = userTXT[0]
    index = 1
    while index < userTXTLen and line[0] != title:
        line = userTXT[index]
        index += 1
    
    if userTXTLen < index:
        return False
    
    with open(os.path.join(inDir, "users", serialStr, str(line[1]) + ".post"), "wb") as f:
        f.write(Encrypt(newText, key))


def Delete(serial: int, key: bytes, title: str) -> bool:
    """Deletes a post.

    Args:
        serial (int): The user's serial number.
        key (bytes): The user's encryption key.
        title (str): The title of the post.

    Returns:
        bool: True if the post has been successfully deleted, False if not.
    """
    import os
    
    inDir = WorkingDir()
    serialStr = str(serial)
    
    try:
        userTXT = GetUserStored(serial, key, "lr")
        
    except:
        return False
    
    if 0 == len(userTXT):
        return False
    
    userTXTLen = len(userTXT)
    line = userTXT[0]
    index = 1
    while index < userTXTLen and line[0] != title:
        line = userTXT[index]
        index += 1
    
    if userTXTLen < index:
        return False

    userTXT.pop(index - 1)

    for i in range(len(userTXT)):
        userTXT[i] = " ".join(userTXT[i]) + "\n"
    
    userTXT = "".join(userTXT)
    
    with open(os.path.join(inDir, "users", serialStr, "user.info"), "wb") as f:
        f.write(Encrypt(userTXT, key))

    os.remove(os.path.join(inDir, "users", serialStr, line[1] + ".post"))
    
    return True