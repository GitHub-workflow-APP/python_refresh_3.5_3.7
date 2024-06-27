import logging
import subprocess
import sys

# Payload: python3 handler_command_injection.py "ls"
class TTSHandler(logging.Handler):
	# Entry point, and model if record is tainted
	def emit(self, record):
		print('emit')
		msg = self.format(record)
		cmd = [msg]
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.STDOUT) # CWEID 78
		# wait for the program to finish
		print(p.stdout.readline())	
		p.communicate()

	# Entry point, and model if record is tainted
	def handler(self, record):
		print('handler' )
		msg = self.format(record)
		cmd = [msg]
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.STDOUT) # CWEID 78
		# wait for the program to finish
		print(p.stdout.readline())	
		p.communicate()

	# Entry point, and model if record is tainted
	def filter(self, record):
		print('filter' )
		msg = self.format(record)
		cmd = [msg]
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.STDOUT) # CWEID 78
		# wait for the program to finish
		print(p.stdout.readline())	
		p.communicate()


def configure_logging():
    h = TTSHandler()
    root = logging.getLogger()
    root.addHandler(h)
    # the default formatter just returns the message
    root.setLevel(logging.DEBUG)

def main(msg):
    # Tainted data is being passed to custom handler
    logging.debug(msg) # CWEID 117

if __name__ == '__main__':
    configure_logging()
    sys.exit(main(sys.argv[1]))
