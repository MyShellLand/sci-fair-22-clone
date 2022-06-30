# import required modules
import asyncio, json, colorama, rsa, time
from colorama import Fore, Back, Style

# decoration
colorama.init()
str = Fore.RED + "\n(¯`·¯`·.¸¸.·´¯`·.¸¸.··´¯)\n( \\                   / )\n ( )" + Fore.YELLOW + Style.BRIGHT + " CalligraphyCoin " + Back.RESET + Fore.RED + "( ) \n  (/                 \\)  \n   (.·´¯`·.¸¸.·´¯`·.¸)   \n" + Style.RESET_ALL + Fore.LIGHTGREEN_EX
print(str)

# CONFIGURABLE SETTINGS
SERVER_PORT = 8888  # don't change this unless there's a good reason to do so
addrs = []  # this should be an array of dictionaries where each dictionary has an ip and a port and a public key, also can store work info here

n = 9954005327276113749618055670576127928136829039699665632702997303689160878225161528753201729111288130168582954961154151994725030844008015311060747943423907
e = 65537

nodeinfo = {
    'ip': '67.170.231.145',
    'pkn': n,
    'pke': e
}

addrs.append(nodeinfo)


# SYSTEM VARIABLES
chain = []
pending = []
(pk, sk) = rsa.newkeys(512)


async def ginput(mess):
    loop = asyncio.get_event_loop()
    content = await loop.run_in_executor(None, input, mess)
    return content


async def main():
    while True:
        userInput = await ginput("tr,bl,ch:\n")
        if userInput == "tr":
            recipient = await ginput("sender: ")
            amount = await ginput("amount: ")

            await send_transaction(recipient, amount)

        elif userInput == "bl":
            create_block()
            print("block created\n")

        elif userInput == "ch":
            print(f"current chain: \n {chain}")


def responder(input, addr):  # this gets called when someone messages you, the return value is your reply
    global pending
    print(input)

    if input['type'] == 'transaction':
        content = input['content']
        transaction = content['transaction']
        signature = content['signature']
        for dict in addrs:
            if dict['addr'] == addr:
                pkn = dict['pkn']
                pke = dict['pke']
                pk = rsa.PublicKey(pkn, pke)


        transactionCoded = json.dumps(transaction).encode()

        verif = rsa.verify(transactionCoded, signature, pk)

        if verif == 'SHA-1':
            pending.append(transaction)
            print("transaction verified!")

            return "transaction verified!"


async def send_transaction(recipient, amount):
    transaction = {
        'sender': pk,
        'recipient': recipient,
        'amount': amount
    }

    transactionBytes = json.dumps(transaction).encode()

    signed = rsa.sign(transactionBytes, sk, 'SHA-1')
    # encodedSignature = base64.b64encode(signed)
    # stringdEncodedSignature = encodedSignature.decode('ascii')

    content = {
        'transaction': transaction,
        'signature': signed
    }

    message = {
        'type': 'transaction',
        'timestamp': time.time(),
        'content': content
    }

    for i in addrs:
        ipAndpk = addrs[i]
        addr = ipAndpk['addr']
        await send(message, addr)


def create_block():
    global pending, chain

    block = {
        'index': (len(chain) + 1),
        'transactions': pending
    }
    pending = []
    chain.append(block)


def find_balance(userID):
    balance = 0

    for i in range(len(chain)):
        block = chain[i]
        transactions = block['transactions']

        for i in range(len(transactions)):
            transaction = transactions[i]
            sender = transaction['sender']
            recipient = transaction['recipient']
            amount = transaction['amount']

            if sender == userID:
                balance = balance - amount
            elif recipient == userID:
                balance = balance + amount
    return balance


# -----------------------------------------FAH

# -----------------------------------------SERVER AND NETWORKING

async def maintain_connection(reader):
    data = []  # collects data
    while True:
        packet = await reader.read(1024)
        data.append(packet.decode("utf-8"))
        if len(packet) < 1024:
            break
    data = json.loads("".join(data))
    return data


async def send(message, addr):
    reader, writer = await asyncio.open_connection(addr, SERVER_PORT)
    writer.write(coder(message))
    writer.close()
    data = await maintain_connection(reader)
    if len(data) > 0:
        print(
            Fore.YELLOW + f"-----Message sent; recieved response from {addr}-----\n" + data + "\n" + "-" * 56 + Fore.LIGHTGREEN_EX)
    else:
        print(Fore.YELLOW + "Sent!" + Fore.LIGHTGREEN_EX)
    return data


def coder(data, encode=True):
    return bytes(json.dumps(data), encoding="utf-8") if encode else json.loads(data.decode("utf-8"))


async def nquery(reader, writer):
    print("New connection")
    addr = writer.get_extra_info('peername')
    data = await maintain_connection(reader)
    print(data)
    reply = responder(data, addr)
    if not reply:
        reply = "Error: no output for responder function."
    writer.write(coder(reply))
    await writer.drain()
    writer.close()


async def sentry():
    server = await asyncio.start_server(nquery, "0.0.0.0", SERVER_PORT)
    async with server:
        await server.serve_forever()


async def booter():  # nice to have this at the end for orginization
    input_coroutines = [sentry(), main()]
    result = await asyncio.gather(*input_coroutines, return_exceptions=True)
    return result


asyncio.run(booter())