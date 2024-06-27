import asyncio
import sys
import subprocess

# Attack Payload: python3 loops.py "ls"
# Note: This testcase doesn't work as desired at runtime... Individual API calls do work, just that process management always seems to create some runtime exceptions.
# We might not be able to find most of the flaws due lack of inter procedural/callable/callback functionality. But, hoping some day we might :)

async def blocking_io(tainted_data):
	p = subprocess.Popen(tainted_data, stdout=subprocess.PIPE,stderr=subprocess.STDOUT) # CWEID 78
	return p.communicate()[0]

def sample_task():
	p = subprocess.Popen(sys.argv[1], stdout=subprocess.PIPE,stderr=subprocess.STDOUT) # CWEID 78
	return p.communicate()[0]

def sample_call_soon(tainted_data) :
	p = subprocess.Popen(tainted_data, stdout=subprocess.PIPE,stderr=subprocess.STDOUT) # CWEID 78
	return p.communicate()[0]

def sample_call_later(tainted_data) :
	p = subprocess.Popen(tainted_data, stdout=subprocess.PIPE,stderr=subprocess.STDOUT) # CWEID 78
	print(p.communicate()[0])

async def main(tainted_data):

	try:
		# run_in_executor
		print('run_in_executor : ', asyncio.get_running_loop().run_in_executor(None, blocking_io,tainted_data))
	except:
		pass

	try :
		# run_until_complete
		loop_until_complete = asyncio.get_event_loop()
		task = loop_until_complete.create_task(sample_task())
		result = loop_until_complete.run_until_complete(task)
		print('run_until_complete : ' , result)
	except:
		pass


	try:
		# call_soon
		event_loop = asyncio.get_event_loop()
		result = event_loop.call_soon(sample_call_soon(sys.argv[1]))
		print('call_soon ' , result)
	except:
		pass

	# call_later
	try:
		# call_later
		event_loop = asyncio.get_event_loop()
		event_loop.call_later(0.1, sample_call_later,sys.argv[1])

	except:
		pass

asyncio.run(main(sys.argv[1]))
