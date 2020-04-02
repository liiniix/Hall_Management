import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/Hall_Management/")
from Hall_Management import app as application
application.secret_key = "sdfsdfg"
