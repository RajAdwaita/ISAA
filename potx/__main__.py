import configparser 
import sys 
from potx import HoneyPot 

#  Import necessary modules:

# configparser is imported for reading configuration settings from the potx.ini file.
# sys is imported for system-related functionality.
# HoneyPot is imported from the potx library, suggesting that this is a custom or third-party library for setting up a honeypot.


# Load config
#  Define the config_filepath variable with the path to the configuration file, which is 'potx.ini'.

config_filepath = 'potx.ini' 
config = configparser.ConfigParser() 
config.read(config_filepath) 
#  Create a config object using ConfigParser to read and parse the configuration file 'potx.ini'.



#  Retrieve configuration settings:

# Read the 'ports' setting from the 'default' section and assign it to the ports variable. If 'ports' is not defined, the fallback value "1234" is used.
# Read the 'host' setting from the 'default' section and assign it to the host variable. If 'host' is not defined, the fallback value "0.0.0.0" is used.
# Read the 'logfile' setting from the 'default' section and assign it to the log_filepath variable. If 'logfile' is not defined, the fallback value "potx.log" is used.



ports = config.get('default', 'ports', raw=True, fallback="1234") 
host = config.get('default', 'host', raw=True, fallback="0.0.0.0") 
log_filepath = config.get('default', 'logfile', raw=True, fallback="potx.log") 

# Double check ports provided

# Check and parse the 'ports' setting:

# Initialize an empty list called ports_list.
# Try to split the 'ports' string using a comma as the delimiter and store the result in ports_list.
# If an exception occurs during the parsing (e.g., invalid input), print an error message and exit the script with an error code of 1.




ports_list = [] 
try: 
    ports_list = ports.split(',') 
except Exception as e: 
    print('[-] Error parsing ports: %s.\nExiting.', ports) 
    sys.exit(1) 

# Launch honeypot

# Create a HoneyPot instance with the host, ports_list, and log_filepath as arguments. It seems like this HoneyPot class from the potx library is responsible for setting up and running a honeypot.



honeypot = HoneyPot(host, ports_list, log_filepath) 

# Run the honeypot:

# Call the run method on the honeypot object to start the honeypot server based on the provided configuration.


honeypot.run() 
