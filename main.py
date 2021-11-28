import Database.Config.config
import _thread as th, subprocess as sp
from Server.server import TCPServer
from Database import initializer
from Controllers.controller import Controller


help_str = '''
start adress port - server starts
stop - server stops
host - returns hostname
clients - return tuple: (adress, port) and amount of clients
threads - return tuple: (thread, th_state) and amount of threads
ctables - create tables
ctriggers - create triggers
initable - initialize tables
info - return server info: adress, port
'''

if __name__ == '__main__':
    db_initializer = initializer.DbInitializer(initializer.Base)
    server = TCPServer(None, None)

    controller = Controller()
    
    while (cmd := input('>> ')) != 'exit': 
        if cmd.startswith('start') and server.active == False:
            inet_info = cmd.split()
            try:
                host, port = inet_info[1], int(inet_info[2])
                server.set_inet_info(host, port)
                server.turn_on()
                th.start_new_thread(server.dispatcher, (controller.perform, ))
            except Exception as e:
                print('Invalid command. Type !help for getting help', e) 
        
        elif cmd.startswith('stop') and server.active == True:
            server.turn_off()

        elif cmd == 'host':
            print('hostname:', server.hostname())

        elif cmd == 'info':
            print('IP-adress: {}, port: {}'.format(*server.inet_info()))

        elif cmd == 'clients':
            clients = server.get_sockets()
            print(len(clients), 'clients')  
            for index, client_inet_info in enumerate(clients):
                print(index, 'client inet info:', client_inet_info) 

        elif cmd == 'threads':
            threads = server.get_threads()
            print(len(threads), 'threads')
            for index, thread in enumerate(threads):
                print(index, 'thread:', thread, 'state', threads[thread].active)
                
        elif cmd == 'ctables':
            db_initializer.create_tables()
            
        elif cmd == 'ctriggers':
           db_initializer.create_triggers()
           
        elif cmd == 'initables':
           db_initializer.init_tables() 
           
        elif cmd == 'help':
            print(help_str)
        
        else:
            if cmd: sp.run(cmd.split())
