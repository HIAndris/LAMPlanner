from modules import postmanager
from modules import filemanager

name = "Jóska"
password = "Jelszó"

postmanager.GetUnameGetHash(name, password)

while True:
    postmanager.MainLoop()

    # print(filemanager.GetUserStored(filemanager.GetUserSerial(name), filemanager.CreateEncryptionKey(name, password), "a"))