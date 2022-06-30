from nacl.signing import SigningKey


#here is the message
message = b"cyka blyat"

# generate keys
sk = SigningKey.generate()
pk = sk.verify_key

#encode public key
serializedpk = pk.encode()

#sign a message
signed = sk.sign(message)


#----------------verify it--------------------

from nacl.signing import VerifyKey

def realVerification(message,serializedpk,signed):

    obj = VerifyKey(serializedpk)
    decoded = obj.verify(signed)

    if decoded == message:
        return 1
    else:
        return 0


doitwork = realVerification(message,serializedpk,signed)


print(sk)
print(pk)
print(serializedpk)
print(doitwork)