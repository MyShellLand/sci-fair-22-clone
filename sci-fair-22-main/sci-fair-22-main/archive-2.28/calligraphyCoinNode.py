import base64
from tracemalloc import start

from p2pnetwork.node import Node
import rsa
import time
import json

class calligraphyCoinNode(Node):
    def __init__(self,host,port,id=None,callback=None,max_connections=0):
        super(calligraphyCoinNode,self).__init__(host,port,id,callback,max_connections)
        # copied from the example because I don't know what I'm doing
        self.chain = []
        self.pending= []
        #initialize chain and pending transactions
        (self.pk,self.sk) = rsa.newkeys(512)
        #generate secret/public key pair

        print(f"node - {self.id} - started")


    def inbound_node_connected(self, node):
        print(node.id + " connected to " + self.id)

    def outbound_node_connected(self, node):
        print(self.id + " connected to " + node.id)


# below are things for transactioners

    def send_transaction(self,recipient,amount):
        transaction = {
            'sender':self.id,
            'recipient':recipient,
            'amount':amount
        }

        transactionBytes = json.dumps(transaction).encode()

        signed = rsa.sign(transactionBytes, self.sk, 'SHA-1')
        encodedSignature = base64.b64encode(signed)
        stringdEncodedSignature = encodedSignature.decode('ascii')

        message = {
            'type':'transaction',
            'timestamp':time.time(),
            'transaction':transaction,
            'signature':stringdEncodedSignature,
            'key':[self.pk.n, self.pk.e]

        }

        self.send_to_nodes(message)
        self.pending.append(transaction)


# below are things for miners
    def node_message(self, node, data): #this is the important one--what does a node do when it receives a message

        print(data)
        if data['type'] =='transaction':
            transaction = data['transaction']
            signature = data['signature']
            keyInts = data['key']
            key = rsa.PublicKey(keyInts[0],keyInts[1])
            decodedTransaction = json.dumps(transaction).encode()
            unstringedSignature = signature.encode('ascii')
            decodedSignature = base64.b64decode(unstringedSignature)


            bruh = rsa.verify(decodedTransaction,decodedSignature,key)
            if bruh == 'SHA-1':
                self.pending.append(transaction)



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

        for i in range(len(self.chain)):
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

    def print_chain(self):
        print(self.chain)





# test w/ multiple computers and live input things

#this part is where it does stuff based on real time input... should be added to the class but alas i am too dumb for that
while True:
    userInput = input("start to start, cn to connect, tr for transaction, bl for block, ch to see chain, stop to stop\n")

    if userInput == "start":
        ip = input("ip: ")
        port = input("port: ")
        port = int(port)
        name = input("name: ")

        node = calligraphyCoinNode(ip, port, name)
        node.start()

    if userInput == "cn":
        cnIp = input("their ip: ")
        cnPort = input("their port: ")
        cnPort = int(cnPort)

        node.connect_with_node(cnIp,cnPort)

    if userInput == "stop":
        node.stop()
        time.sleep(5)
        break
    if userInput == "tr":

        recipient = input("recipient: ")
        amount = input("amount: ")

        node.send_transaction(recipient,amount)
        print("sent!\n")

    if userInput == "bl":
        node.create_block()
        print("block created!\n")

    if userInput == "ch":
        print("chain:\n")
        node.print_chain()
