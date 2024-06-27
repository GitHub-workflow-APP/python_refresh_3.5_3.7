import threading
import sys
import subprocess

class FunctCall:
	def thread_function(self,args):
		p = subprocess.Popen(args, stdout=subprocess.PIPE,stderr=subprocess.STDOUT) # CWEID 78
		print(p.communicate()[0])

if __name__ == "__main__":
	funct_call = FunctCall()
	x = threading.Thread(target=funct_call.thread_function, args=(sys.argv[1],))
	x.start()
