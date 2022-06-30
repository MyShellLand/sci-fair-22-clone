
import asyncio, json, socket, colorama
from colorama import Fore, Back, Style
ip_addr = socket.gethostbyname(socket.gethostname())
colorama.init()

#decoration
str = Fore.RED+"\n(¯`·¯`·.¸¸.·´¯`·.¸¸.··´¯)\n( \\                   / )\n ( )"+Fore.YELLOW+Style.BRIGHT+" CalligraphyCoin "+Back.RESET+Fore.RED+"( ) \n  (/                 \\)  \n   (.·´¯`·.¸¸.·´¯`·.¸)   \n"+Style.RESET_ALL+Fore.LIGHTGREEN_EX
print(str)

# runs at the beginning of the program
async def ginput(mess):
    loop = asyncio.get_event_loop()
    content = await loop.run_in_executor(None, input, mess)
    return content

async def main():
    while True:
        await ginput(f"[{ip_addr}] Press enter to send a message...")
        input = await ginput("Enter message: ")
        address = await ginput("Send to whoom: ")
        if address == "":
            address = "127.0.0.1"
        try:
            await asyncio.wait_for(send(input, address), timeout=1.0)
        except:
            print(Fore.RED+"Error: could not connect"+Fore.LIGHTGREEN_EX)

def responder(input): # this gets called when someone messages you, the return value is your reply
    return f"Thanks for your message, you've reached {ip_addr}. By the way, your message was {len(input)} characters long."

#fancy code---------------------------------------

async def send(message, addr):
    reader, writer = await asyncio.open_connection(addr, 4321)
    writer.write(coder(message))

    data = [] # collects data
    while True:
        packet = await reader.read(1024)
        data.append(packet.decode("utf-8"))
        if len(packet) < 1024:
            break
    data = json.loads("".join(data))
    writer.close()
    if len(data)>0:
        print(Fore.YELLOW+f"-----Message sent; recieved response from {addr}-----\n"+data+"\n"+"-"*56+Fore.LIGHTGREEN_EX)
    else:
        print(Fore.YELLOW+"Sent!"+Fore.LIGHTGREEN_EX)
    return data 

def coder(data, encode=True):
    return bytes(json.dumps(data), encoding="utf-8") if encode else json.loads(data.decode("utf-8"))

async def nquery(reader, writer):
    addr = writer.get_extra_info('peername')
    data = [] # collects data
    while True:
        packet = await reader.read(1024)
        data.append(packet.decode("utf-8"))
        print(packet)
        if len(packet) < 1024:
            break
    data = json.loads("".join(data))
    print(Fore.MAGENTA+f"-----New message from {addr}--------------\n", data, "\n"+"-"*56+Fore.LIGHTGREEN_EX)

    reply = responder(data)
    if not reply:
        reply = "I was too lazy to write an actual reply."

    writer.write(coder(reply))
    await writer.drain()
    writer.close()

async def sentry():
    server = await asyncio.start_server(nquery, "0.0.0.0", 4321)
    async with server:
        await server.serve_forever()


async def booter():
    input_coroutines = [sentry(), main()]
    result = await asyncio.gather(*input_coroutines, return_exceptions=True)
    return result

asyncio.run(booter())