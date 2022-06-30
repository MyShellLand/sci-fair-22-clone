import asyncio, json
        
def coder(data, encode=True):
    return bytes(json.dumps(data), encoding="utf-8") if encode else json.loads(data.decode("utf-8"))



asyncio.run(tcp_echo_client('Hello World!'))