import _thread as th, os
from Server.server import TCPServer
from Database import initializer

if __name__ == '__main__':
    #db_initializer = initializer.DbInitializer(initializer.Base)
    #db_initializer.create_tables()
    #db_initializer.create_triggers()
    #db_initializer.init_tables()
    server = TCPServer(None, None)
    
    while (cmd := input('>> ')) != 'exit': 
        if cmd.startswith('start') and server.active == False:
            inet_info = cmd.split()
            try:
                host, port = inet_info[1], int(inet_info[2])
                server.set_inet_info(host, port)
                server.turn_on()
                th.start_new_thread(server.dispatcher, (client_handler,))
            except Exception as e:
                print('Invalid command. Type !help for getting help', e) 
        
        elif cmd.startswith('stop') and server.active == True:
            server.turn_off()

        elif cmd == 'host':
            print('hostname:', server.hostname())

        elif cmd == 'clients':
            clients = server.get_sockets()
            print(len(clients), 'clients')  
            for index, client_inet_info in enumerate(clients):
                print(index, 'client inet info:', client_inet_info)

        elif cmd == 'info':
            print('IP-adress: {}, port: {}'.format(*server.inet_info()))

        elif cmd == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
       
        elif cmd == 'threads':
            threads = server.get_threads()
            print(len(threads), 'threads')
            for index, thread in enumerate(threads):
                print(index, 'thread:', thread, 'state', threads[thread].active)
        else:
            print('Invalid command. Type !help for getting help')
