import cryptography
from cryptography.fernet  import Fernet
key = Fernet.generate_key()
print(key)
def apexcrypting1():
    f = Fernet(key)

    toencrypt = bytes(input("Please enter your text to be encrypted"), 'utf-8')

    encrypted = f.encrypt(toencrypt)
    print(toencrypt)
    print(encrypted)
    decrypted = f.decrypt(encrypted)

    print(decrypted)




