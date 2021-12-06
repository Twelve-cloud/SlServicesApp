from threading import Thread
from socket import AF_INET, SOCK_STREAM, \
            SOL_SOCKET, SO_REUSEADDR,    \
            SHUT_RDWR, socket, inet_aton
from Logger.logger import Logger

logger = Logger('logs', 'server_logs.txt')

class TCPServer:
    def __init__(self):
        self.host = None
        self.port = None
        self.clients = {}
        self.threads = {}
        self.active = False

    def set_inet_info(self, host, port):
        if host != 'localhost':
            inet_aton(host)
            
        if port < 1023 or port > 49152:
            raise 'Invalid port'
        
        self.host = host
        self.port = port

    def get_inet_info(self):
        return (self.host, self.port)

    def is_active(self):
        return self.active

    def turn_on(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(100)
        self.active = True
        logger.write(
            f'Server has been listening at '
            f'address: {self.host}, port: {self.port}'
        )

    def turn_off(self, dispatcher_thread):
        for connection in self.clients:
            connection.shutdown(SHUT_RDWR)
            self.threads[connection].join()
            connection.close()
        
        self.sock.shutdown(SHUT_RDWR)
        self.sock.close()
        self.clients = {}
        self.threads = {}
        self.active = False
        dispatcher_thread.join()
        logger.write('Server has stoppped')

    def dispatcher(self, client_function):
        while True:
            try:
                connection, address = self.sock.accept()
                self.add_client(connection, address)
                
                thread = Thread(
                    target = client_function,
                    args = (connection, self)
                )
                self.add_thread(connection, thread)
                thread.start()
            except Exception:
                logger.write('Accept function was inturrupted')
                break

    def add_client(self, connection, address):
        self.clients[connection] = address
        logger.write('Server connected by' +  str(address))

    def del_client(self, connection):
        address = self.clients.pop(connection)
        logger.write('Client ' + str(address) + ' has disconnected')

    def get_clients(self):
        return self.clients
        
    def add_thread(self, connection, thread):
        self.threads[connection] = thread
        
    def del_thread(self, connection):
        self.threads.pop(connection)

    def get_threads(self):
        return self.threads
