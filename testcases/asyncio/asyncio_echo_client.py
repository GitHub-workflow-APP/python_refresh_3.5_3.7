import asyncio
import sys
import subprocess

# Attack payload: python3 asyncio_echo_client.py "ls"
# Works in conjuction with asyncio_echo_server

# Should be treated as a function call
async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection('', 8888) # CWEID 923

    print(f'Send: {message!r}')
    writer.write(message.encode()) # CWEID 201
    await writer.drain()

    data = await reader.read(100) # <--- Network.Tainted SOURCE
    #print(f'Received: {data.decode()!r}')

    p = subprocess.Popen(data, stdout=subprocess.PIPE,stderr=subprocess.STDOUT) # CWEID 78
    print(p.communicate()[0])

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_echo_client(sys.argv[1]))
