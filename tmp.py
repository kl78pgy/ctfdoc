import hashlib
sha256 = hashlib.sha256()
sha256.update("flag{678}".encode('utf-8'))
res = sha256.hexdigest()
print (res)