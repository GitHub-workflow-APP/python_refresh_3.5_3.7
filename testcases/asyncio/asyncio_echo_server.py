import asyncio
import sys

# Attack Payload: python3 asyncio_echo_server.py 'localhost'
# Works in conjuction with asyncio_echo_client.py

# Configured as callback, should be treated as function call with first argument as tainted
async def handle_echo(reader, writer):
    data = await reader.read(100) # <-- Network.Tainted SOURCE
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    print(f"Send: {message!r}")
    writer.write(data) # CWEID 201
    await writer.drain()

    print("Close the connection")
    writer.close()

# Should be treated as function
async def main():
    server = await asyncio.start_server(
        handle_echo, sys.argv[1], 8888) # CWEID 99

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())