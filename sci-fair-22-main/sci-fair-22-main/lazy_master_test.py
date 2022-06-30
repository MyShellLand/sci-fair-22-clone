
import asyncio, colorama, logging
from colorama import Fore
from gateway import Radio
from node import Node

logging.basicConfig(filename='debug.log', format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s", level=logging.DEBUG)
logging.info('===========================================PROGRAM STARTED================================')
colorama.init()
SERVER_PORT = 8888
COMPANIONS = ["10.0.0.245","10.0.0.234","10.0.0.88", "10.0.0.176","10.0.0.228","10.0.0.117", "10.0.0.234"]

# in this version, the api calls are replaced by calling variables that can be changed by user input
current_fake_work_data = []  # this is what get_members returns, it should have 5 columns
current_fake_team_data = []  # this is what team_info returns

async def ginput(m):
    logging.debug("Getting new user input")
    return await asyncio.get_event_loop().run_in_executor(None, input, m)


def responder(input, addr):
    if input['type'] == 'block':
        if USR_NODE.lazy_process(input, addr) is True:
            return "confirmation"
    elif input['type'] == 'genesis' or input['type'] == 'introduction':
        if USR_NODE.process_message(input,addr) is True:
            return "confirmation"
    else:
        print("too lazy to respond to that kind of message")


async def main(): # GUI here
    global current_fake_work_data, current_fake_team_data


    if USR_NODE.nickname == "Anonymous":
        USR_NODE.setnick(await ginput("Hi there! Please set your nickname: "))
    print(
        f"Welcome, {USR_NODE.nickname}. Enter h for help, use {Fore.LIGHTWHITE_EX}Ctrl+C{Fore.LIGHTGREEN_EX} to exit.")
    while True:
        userInput = await ginput("in,tr,ch,bk,co,wd,td:\n")
        if userInput == "tr":
            recipient = await ginput("recipient: ")
            amount = await ginput("amount: ")
            message = USR_NODE.transaction(recipient, amount)
            print(f"message generated:{message}")

            await SERVER.send_all(COMPANIONS, message)

        elif userInput == "ch":
            print(f'visualization file is at: {USR_NODE.visualize_chain()}')
            print(f"current chain as heard: \n {USR_NODE.heard_chain}")
            print(f'self chain should be empty: \n {USR_NODE.chain}')

        elif userInput == "bk":
            logging.debug("backing up user data")
            USR_NODE.backup_data()

        elif userInput == "co":
            print(USR_NODE.contacts)

        elif userInput == "in":
            await SERVER.send_all(COMPANIONS,USR_NODE.introduce_self())

        elif userInput == 'wd':
            ids = await ginput("comma-delineate ids (pks)")
            works = await ginput("comma-delineate respective total works")
            current_fake_work_data = [["name","id","rank","score","wus"]]
            idss = ids.split(",")
            workss = works.split(",")

            for i in range(len(idss)):
                row = [idss[i],0,0,0,int(workss[i])]
                current_fake_work_data.append(row)

            logging.debug(f'created fake api current data: {current_fake_work_data}')


        elif userInput == 'td':
            score = await ginput("total score rn? (just for seeding purposes)")
            current_fake_team_data = {
                'score':int(score)
            }
            logging.debug(f'created fake team data for seeding: wus = {score}')

        elif userInput == "help" or userInput == "h":
            print("""
            in: introduces yourself to other nodes by sending them your public key
            gn: creates a genesis block where you can define what the work done at that point was
            tr: creates a new transaction and sends it to the other nodes
            sbl: sends out the block that you have generated
            ch: helps visualize the chain
            bk: backs up your chain, keys, and other data to a storage file
            co: prints out your contacts
            td: allows you to set a seed for rng
            wd: allows you to fake work being done by 
            """)



async def tester():
    print(USR_NODE.easy_miner_decider(current_fake_team_data,current_fake_work_data,number_of_winners=1))


async def booter():
    await asyncio.gather(SERVER.sentry(), main())

SERVER = Radio(responder, port=SERVER_PORT)
USR_NODE = Node()
SERVER.welcome()

asyncio.run(booter())