import asyncio, json, logging
from urllib import request
from colorama import Fore, Back, Style

class Radio:
    def __init__(self, responder, port=8888):
        logging.debug("Initializing new Radio class")
        self.responder = responder
        self.port = port

    def encode(self, data):
        logging.debug("encoding")
        return bytes(json.dumps(data), encoding="utf-8")

    async def handle_conn(self, reader):
        logging.debug("Handling new connection...")
        data = [] # collects data
        while True:
            packet = await reader.read(1024)
            data.append(packet.decode("utf-8"))
            logging.debug(f"New packet recieved >{packet}<")
            if len(packet) < 1024:
                logging.debug("breaking")
                break
        logging.debug(f"jsoning data >{data}<")
        data = json.loads("".join(data))
        logging.debug("Data compiled")
        return data

    async def send(self, message, addr):
        logging.debug("Sending new message")
        reader, writer = await asyncio.open_connection(addr, self.port)
        logging.debug("Connection opened, encoding")
        encoded = self.encode(message)
        logging.debug(f"Encoded >{encoded}<")
        writer.write(encoded)
        logging.debug("Data transmitted...")
        data = await self.handle_conn(reader)
        writer.close()
        logging.debug("Finished sending, returning response")
        return data

    async def send_all(self, ipaddr_list, message):
        logging.debug("Sending message to list of ips")
        replies = []
        for addr in ipaddr_list:
            replies.append(asyncio.wait_for(self.send(message, addr), timeout=1))
        responses = await asyncio.gather(*replies, return_exceptions=True)
        logging.debug(f"All responses recieved-------------\n\n{responses}")
        return responses

    async def nquery(self, reader, writer):
        logging.debug("New connection recieved")
        addr = writer.get_extra_info('peername')
        data = await self.handle_conn(reader)
        reply = self.responder(data, addr)
        logging.debug("Recieved reply from responder function")
        if not reply:
            reply = "no reply provided"
        writer.write(self.encode(reply))
        await writer.drain()
        writer.close()
        logging.debug("Reply sent to peer")

    async def sentry(self):
        logging.debug("Starting server")
        server = await asyncio.start_server(self.nquery, "0.0.0.0", self.port)
        logging.debug("Server started")
        async with server:
            await server.serve_forever()
    
    def welcome(self):
        logging.debug("Printing welcome message")
        str = Fore.RED+"\n(¯`·¯`·.¸¸.·´¯`·.¸¸.··´¯)\n( \\                   / )\n ( )"+Fore.YELLOW+Style.BRIGHT+" CalligraphyCoin "+Back.RESET+Fore.RED+"( ) \n  (/                 \\)  \n   (.·´¯`·.¸¸.·´¯`·.¸)   \n"+Style.RESET_ALL+Fore.LIGHTGREEN_EX
        print(str)


