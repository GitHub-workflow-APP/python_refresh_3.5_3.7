#importing module 
import logging 
import sys
  
#Create and configure logger 
logging.basicConfig(filename="newfile.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 
  
#Creating an object 
logger=logging.getLogger() 
  
#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG) 
  
#Test messages 
logger.debug(sys.argv[1]) # CWEID 117
logger.info(sys.argv[1]) # CWEID 117
logger.warning(sys.argv[1]))  # CWEID 117
logger.error(sys.argv[1])  # CWEID 117
logger.critical(sys.argv[1]) # CWEID 117
