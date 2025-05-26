from cryptography.fernet import Fernet

key = b'tfn8u9wMbSl1etTRn5SSY3mK-GpQtpT1JUFxng4xywE='
f = Fernet(key)

with open('imp_1', 'rb') as orignal:
   orignal_files = orignal.read()
orignal1 = bytes(orignal_files)




with open('data.json','wb') as encrypt:

    orignal1 = f.decrypt(orignal1)
    encrypt.write(orignal1)