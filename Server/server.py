import threading, time, os
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SHUT_RDWR, socket, inet_aton, gethostname
from .state import State
from Logger.logger import Logger

logger = Logger('logs', 'server_logs.txt')

class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_sockets = {}
        self.threads = {}
        self.active = False

    def set_inet_info(self, host, port):
        if host != 'localhost':
            inet_aton(host)
            
        if port < 1023 or port > 49152:
            raise 'Invalid port'
        
        self.host = host
        self.port = port

    def turn_on(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(100)
        self.active = True
        logger.write('Server has been listening')

    def turn_off(self):
        for cl_sock in self.client_sockets.copy():
            self.remove_socket(cl_sock)
        
        for thread in self.threads:
            self.thread_off(thread)
        
        self.sock.shutdown(SHUT_RDWR)
        self.sock.close()
        self.client_sockets = {}
        self.threads = {}
        self.active = False
        logger.write('Server has stoppped')

    def dispatcher(self, handle_client):
        while True:
            try:
                client_socket, address = self.sock.accept()
                logger.write('Server connected by' +  str(address))
                self.add_socket(address, client_socket)
                
                thread_state = State(active = True)
                thread = threading.Thread(target = handle_client, args = (client_socket, thread_state))
                self.thread_on(thread, thread_state)
            except Exception: pass

    def add_socket(self, address, client_socket):
        self.client_sockets[address] = client_socket

    def remove_socket(self, address):
        if not (client_socket := self.client_sockets.pop(address, False)):
            logger.write('Cannot remove client socket ' + str(address) + ': not exist')
        else:
            client_socket.close()
            logger.write('Client ' + str(address) + ' has disconnected')

    def get_sockets(self):
        return self.client_sockets

    def thread_on(self, thread, thread_state):
        self.threads[thread] = thread_state
        thread.start()

    def thread_off(self, thread):
        self.threads[thread].active = False
        thread.join()

    def get_threads(self):
        return self.threads

    def hostname(self):
        return gethostname()

    def inet_info(self):
        return (self.host, self.port)
