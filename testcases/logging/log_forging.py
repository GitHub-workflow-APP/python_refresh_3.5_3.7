import logging
import logging.handlers
import sys

	
def init_stream_handler():
	sh = logging.StreamHandler()
	logging.getLogger().addHandler(sh)
	logging.getLogger().setLevel(logging.INFO)

	return logging

def init_file_handler(logfile):
	fh = logging.FileHandler(logfile)
	formatter = logging.Formatter('%(asctime)s %(message)s')
	fh.setFormatter(formatter)
	logging.getLogger().addHandler(fh)
	logging.getLogger().setLevel(logging.INFO)

	return logging

logger_stream = init_stream_handler()
logger_file = init_file_handler('logfile.txt')

# logger_steam, logger_file should return logging object, and thus existing sinks should work
# Technically, these are FPs. All specialized loggers (Stream, File, Null) and custom loggers are CRLF Injection safe. However, its bit more work for differentiate between loggers, so leaving it alone. If customers complain about FPs, we can further improve support
logger_stream.info("Logger Stream " + sys.argv[1]) # CWEID 117
logger_file.info("Logger File " + sys.argv[1]) # CWEID 117


class CustomHandler(logging.Handler):
	def __init__(self):
		pass

	def emit(self, record):
		print('Emit' + record)
		msg = self.format(record)
		#stream = self.stream
	def filter(self, record):
		print('Filter' + record)

	def format(self,record):
		print('Format ' + record)
	def handle(self,record):
		print('handle' + record)
	

def config_logger():
	custom_handler = CustomHandler()
	root = logging.getLogger('root')
	root.setLevel(logging.INFO)
	root.addHandler(custom_handler)


config_logger()
logging.info("Custom Handler " + sys.argv[1]) # CWEID 117
