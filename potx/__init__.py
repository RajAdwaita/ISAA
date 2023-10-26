import logging 
import threading 
from socket import socket, timeout 

# Import Necessary Modules:

# Import the logging module for handling logging.
# Import the threading module for managing multiple threads.
# Import the socket module and the timeout exception for working with network sockets.


class HoneyPot(object): 
    
    # a. __init__(self, bind_ip, ports, log_filepath):

# Class constructor that initializes the HoneyPot object.
# Parameters:
# bind_ip: The IP address to which the honeypot should bind.
# ports: A list of port numbers on which the honeypot should listen.
# log_filepath: The path to the log file for recording honeypot activity.
# It checks whether at least one port is provided; otherwise, it raises an exception.
# Initializes instance attributes:
# bind_ip to the provided IP address.
# ports to the provided list of port numbers.
# log_filepath to the provided log file path.
# listener_threads as an empty dictionary for managing listener threads.
# logger by calling the prepare_logger method to set up the logging configuration.

    def __init__(self, bind_ip, ports, log_filepath): 
        if len(ports) < 1: 
            raise Exception("No ports provided.") 

        self.bind_ip = bind_ip 
        self.ports = ports 
        self.log_filepath = log_filepath 
        self.listener_threads = {}  
        self.logger = self.prepare_logger() 

        self.logger.info("Honeypot initializing...") 
        self.logger.info("Ports: %s" % self.ports) 
        self.logger.info("Log filepath: %s" % self.log_filepath) 
        
        # b. handle_connection(self, client_socket, port, ip, remote_port):

# Handles incoming connections to the honeypot.
# Parameters:
# client_socket: The socket object representing the client connection.
# port: The port number on which the connection was received.
# ip: The IP address of the client.
# remote_port: The remote port of the client.
# Logs the connection information.
# Sets a timeout of 10 seconds on the client_socket.
# Tries to receive data from the client (up to 4096 bytes) and logs it.
# Sends an "Access denied" message back to the client.
# Closes the client_socket.

    def handle_connection(self, client_socket, port, ip, remote_port): 
        self.logger.info("Connection received: %s: %s:%d" % 
                         (port, ip, remote_port)) 

        client_socket.settimeout(10) 
        try: 
            data = client_socket.recv(4096) 
            self.logger.info("Data received: %s: %s:%d: %s" % 
                             (port, ip, remote_port, data)) 
            client_socket.send("Access denied.\n".encode('utf8')) 
        except timeout: 
            pass 
        client_socket.close() 
        
        # c. start_new_listener_thread(self, port):

# Creates a new listener thread for a specified port.
# Parameters:
# port: The port to listen on.
# Creates a socket, binds it to the provided IP and port, and listens for incoming connections.
# In an infinite loop, it accepts incoming client connections.
# For each connection, it starts a new thread (client_handler) to handle the connection by calling the handle_connection method.

    def start_new_listener_thread(self, port): 
        # Create a new listener
        listener = socket()   # Defaults (socket.AF_INET, socket.SOCK_STREAM)
        listener.bind((self.bind_ip, int(port))) 
        listener.listen(5) 
        while True: 
            # client: The socket representing the client connection.
            # port: The port on which the connection was received.
            # addr[0]: The IP address of the client.
            # addr[1]: The remote port of the client.
            client, addr = listener.accept() 
            client_handler = threading.Thread( 
                target=self.handle_connection, args=(client, port, addr[0], addr[1]))
            client_handler.start() 
            
            # In summary, this piece of code accepts incoming client connections, creates a separate thread for each connection, and starts the thread to handle the connection using the handle_connection method. This allows the honeypot to handle multiple client connections concurrently.
            
            # d. start_listening(self):

# Starts listener threads for each port specified in the ports attribute.
# Creates a thread for each port and starts it. These threads will run the start_new_listener_thread method.

    def start_listening(self): 
        for port in self.ports: 
            self.listener_threads[port] = threading.Thread( 
                target=self.start_new_listener_thread, args=(port,)) 
            self.listener_threads[port].start() 
            
            # e. run(self):

# This method is used to start the honeypot.
# It simply calls the start_listening method to begin listening on the specified ports.

    def run(self): 
        self.start_listening() 
        
        #  f. prepare_logger(self):

# Sets up the logging configuration.
# Defines a logger that logs messages to both a file (specified by log_filepath) and the console.
# Returns the logger.

    def prepare_logger(self): 
        logging.basicConfig(level=logging.DEBUG, 
                            format='%(asctime)s %(levelname)-8s %(message)s', 
                            datefmt='%Y-%m-%D %H:%M:%S', 
                            filename=self.log_filepath, 
                            filemode='w') 
        logger = logging.getLogger(__name__) 

        # Adding console handler
        console_handler = logging.StreamHandler() 
        console_handler.setLevel(logging.DEBUG) 
        logger.addHandler(console_handler) 
        return logger 


# This setup allows log messages to be displayed on the console as well as written to a log file, making it useful for monitoring and debugging the honeypot's activity while it's running.




