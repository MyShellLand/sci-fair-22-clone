import json

#i wonder if i can make the good code, but worse

index = 0
pending_transactions = []

block = {
    'index': index,
    'transactions': pending_transactions
}

chain = [block]

#make a bunch of variables because objects are hard


def new_transaction(sender,recipient,amount):

    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }

    pending_transactions.append(transaction)

    return transaction

#function to create a transaction based on inputs, and adds it to the pending transactions list

def new_block(pending_transactions):

    index = 1
    block = {
        'index': index,
        'transactions':pending_transactions
    }

    pending_transactions = []

    chain.append(block)

    return block

#function to create a new block based on pending transactions, and add it to the chain


#------------------------------------------------------changing stuff-----------------------------------------

t1 = new_transaction("a","b",20)
t2 = new_transaction("b","a",15)
b = new_block(pending_transactions)


print(chain)
print(pending_transactions)