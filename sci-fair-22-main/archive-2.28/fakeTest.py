import json
from nacl.signing import SigningKey
from nacl.signing import VerifyKey


#this simulates three parties--two doing a transaction and one updating the blockchain based on what they heard


#this is just the blockchain code
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

    def heard_transaction(self,transaction):
        self.pending.append(transaction)

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




# let's just say cyril the spectator has existing a starting blockchain

cyril = bLoCkcHaiN()

t1 = cyril.new_transaction('michaek','cyril',69)
t2 = cyril.new_transaction('cyreal','micheak',420)
t3 = cyril.new_transaction('tristea','cyril',42069)

chain = cyril.create_block()

t1 = cyril.new_transaction('micheakek','curearek',1412438)
t2 = cyril.new_transaction('madfdk','michaek',124)

chain = cyril.create_block()





#here michael wants to propose a transaction--he creates a transaction and broadcasts it
michael = bLoCkcHaiN()
transaction = michael.new_transaction('tristan','michael',250)

#this is what he would send out over the network
michaelBroadcast = bytes(json.dumps(transaction),'utf-8')




#here tristan receives the broadcast, signs it using his secret key, and broadcasts the signature
#secret key and public key is generated here, though they should already exist, and the public key should be publicly known
sk = SigningKey.generate()
pk = sk.verify_key
serializedpk = pk.encode()


#this is what the signer would broadcast
tristanBroadcast = sk.sign(michaelBroadcast)




#cyril is a miner looking to update his pending pool, so verifies the validity of the signature

def verifySignature(message,serializedpk,signed):

    cyril = VerifyKey(serializedpk)
    decoded = cyril.verify(signed)

    if decoded == message:
        return True
    else:
        return False

verdict = verifySignature(michaelBroadcast,serializedpk,tristanBroadcast)

#cyril adds the block to his list of pending transactions if it is verified
if verdict:
    decoded = json.loads(michaelBroadcast)
    cyril.heard_transaction(decoded)

#he then makes a new block
chain = cyril.create_block()
michaels_money = cyril.find_balance("michael")
print(michaels_money)