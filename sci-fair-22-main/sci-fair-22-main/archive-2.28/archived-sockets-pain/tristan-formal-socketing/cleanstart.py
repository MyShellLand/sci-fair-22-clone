import asyncio, json



async def handle_echo(reader, writer):
    print("new connection")
    data = []
    while True:
        packet = await reader.read(1024)
        data.append(packet.decode("utf-8"))
        if len(packet) <1024:
            break
    data = json.loads("".join(data))
    print("got data")
    message = data
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    print(f"Send: {message!r}")
    writer.write(bytes(data, encoding="utf-8"))
    await writer.drain()

    print("Close the connection")
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 4321)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())