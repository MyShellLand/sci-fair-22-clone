
import asyncio, colorama, logging
from colorama import Fore
from gateway import Radio
from node import Node
from api import Foldapi
colorama.init()
logging.basicConfig(filename='debug.log', format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s", level=logging.DEBUG)
logging.info('===========================================PROGRAM STARTED================================')

SERVER_PORT = 8888
COMPANIONS = ["10.0.0.245","10.0.0.234","10.0.0.88", "10.0.0.176","10.0.0.228","10.0.0.117", "10.0.0.234"]

async def ginput(m):
    logging.debug("Getting new user input")
    return await asyncio.get_event_loop().run_in_executor(None, input, m)

def responder(input, addr):
    if USR_NODE.process_message(input, addr) == True:
        return "confirmation"



async def main(): # GUI here
    
    if USR_NODE.nickname == "Anonymous":
        USR_NODE.setnick(await ginput("Hi there! Please set your nickname: "))
    print(f"Welcome, {USR_NODE.nickname}. Enter h for help, use {Fore.LIGHTWHITE_EX}Ctrl+C{Fore.LIGHTGREEN_EX} to exit.")
    while True:

        userInput = await ginput(">>>")
        if userInput == "tr":
            recipient = await ginput("recipient: ")
            amount = await ginput("amount: ")
            message = USR_NODE.transaction(recipient, amount)
            print(f"message generated:{message}")

            await SERVER.send_all(COMPANIONS, message)

        elif userInput == "bl":
            message = USR_NODE.create_block(await fAPI.get_members("CalligraphyCoin"), await fAPI.team_info("CalligraphyCoin"))
            print(f"message generated:{message}")

        elif userInput == "sbl":
            winners = USR_NODE.winners
            if winners.count(USR_NODE.pk) > 0:
                await SERVER.send_all(COMPANIONS,USR_NODE.next_block)
            else:
                print("you weren't chosen, sorry")

        elif userInput == "ch":
            print(f'visualization file is at: {USR_NODE.visualize_local_chain()}')
            print(f"current chain: \n {USR_NODE.chain}")

        elif userInput == "bk":
            logging.debug("backing up user data")
            USR_NODE.backup_data()

        elif userInput == "gn":
            logging.debug("making fake stuff")

            users = await ginput("comma-delineate the pks: ")
            works = await ginput("comma delineate the money to give to each respectively: ")

            pks = users.split(",")
            works = works.split(",")

            money_apparate = []

            for i in range(len(pks)):
                money_apparate.append({
                    'id':pks[i],
                    'amount':float(works[i])
                })

            msg = USR_NODE.genesis(money_apparate)

            await SERVER.send_all(COMPANIONS,msg)

        elif userInput == "co":
            print(USR_NODE.contacts)

        elif userInput == "in":
            await SERVER.send_all(COMPANIONS,USR_NODE.introduce_self())
        elif userInput == "help" or userInput == "h":
            print("""
            in: introduces yourself to other nodes by sending them your public key
            gn: creates a genesis block where you can define what the work done at that point was
            tr: creates a new transaction and sends it to the other nodes
            bl: creates a new block
            sbl: sends out the block that you have generated
            ch: helps visualize the chain
            bk: backs up your chain, keys, and other data to a storage file
            co: prints out your contacts
            """)

async def tester():
    print(USR_NODE.easy_miner_decider(await fAPI.team_info("CalligraphyCoin"),await fAPI.get_members("CalligraphyCoin"),number_of_winners=2))


async def booter():
    await asyncio.gather(SERVER.sentry(), main())

SERVER = Radio(responder, port=SERVER_PORT)
fAPI = Foldapi()
USR_NODE = Node()
SERVER.welcome()

asyncio.run(booter())