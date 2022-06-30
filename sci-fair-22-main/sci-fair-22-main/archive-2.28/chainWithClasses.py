import json
from nacl.signing import SigningKey
from nacl.signing import VerifyKey


class bLoCkcHaiN(object):
    def __init__(self):
        self.chain = []
        self.pending = []

    def new_transaction(self,sender,recipient,amount):
        transaction = {
            'index': len(self.pending)+1,
            'sender':sender,
            'recipient':recipient,
            'amount':amount
        }

        self.pending.append(transaction)
        return transaction

    def create_block(self):
        block = {
            'index':len(self.chain)+1,
            'transactions':self.pending
        }

        self.pending = []
        self.chain.append(block)
        return self.chain

    def find_balance(self,username):

        balance = 0

        for i in range(len(chain)):
            block = self.chain[i]
            transactions = block['transactions']

            for i in range(len(transactions)):
                transaction = transactions[i]
                sender = transaction['sender']
                recipient = transaction['recipient']
                amount = transaction['amount']

                if sender == username:
                    balance = balance - amount
                elif recipient == username:
                    balance = balance + amount


        return balance



# test for recording transactions and then finding balance

obj = bLoCkcHaiN()

t1 = obj.new_transaction('michaek','cyril',69)
t2 = obj.new_transaction('cyreal','micheak',420)
t3 = obj.new_transaction('tristea','cyril',42069)

chain = obj.create_block()

t1 = obj.new_transaction('micheakek','curearek',1412438)
t2 = obj.new_transaction('madfdk','michaek',124)

chain = obj.create_block()


balance = obj.find_balance("michaek")

print(balance)

#signing a transaction and then verifying the signature


#this is what the proposer would broadcast
stringifiedBlock = bytes(json.dumps(t2),'utf-8')


sk = SigningKey.generate()
pk = sk.verify_key
serializedpk = pk.encode()

#this is what the signer would broadcast
signed = sk.sign(stringifiedBlock)


#this is what a spectator would do to verify it
def verifySignature(message,serializedpk,signed):

    obj = VerifyKey(serializedpk)
    decoded = obj.verify(signed)

    if decoded == message:
        return 1
    else:
        return 0


verdict = verifySignature(stringifiedBlock,serializedpk,signed)

print(verdict)