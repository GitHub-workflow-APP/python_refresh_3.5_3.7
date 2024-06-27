import asyncio
import sys

# Co-routines should still be treated as function calls
async def run(code):

    print ("In run" , code)

    proc = await asyncio.create_subprocess_exec(
        sys.executable, '-c', code,
        stdout=asyncio.subprocess.PIPE) # CWEID 78

    stdout, stderr = await proc.communicate()

    #print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

asyncio.run(run(sys.argv[1]))
