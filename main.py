import Database.Config.config
import subprocess as sp
from threading import Thread
from Server.server import TCPServer
from Database.initializer import DbInitializer
from Controllers.controller import Controller


if __name__ == '__main__':
    db_initializer = DbInitializer()
    server = TCPServer()
    dispatcher_thread = None

    controller = Controller()
    
    while (cmd := input('>> ')) != 'exit': 
        if cmd.startswith('start') and not server.is_active():
            inet_info = cmd.split()
            try:
                host, port = inet_info[1], int(inet_info[2])
                
                server.set_inet_info(host, port)
                server.turn_on()
                
                dispatcher_thread = Thread(
                    target = server.dispatcher, 
                    args = (controller.perform, )
                )
                dispatcher_thread.start()
            except Exception as e:
                print('Invalid command. Type !help for getting help')     
        elif cmd.startswith('stop') and server.is_active():
            server.turn_off(dispatcher_thread)
        elif cmd == 'inet info':
            print('IP-adress: {}, port: {}'.format(*server.inet_info()))
        elif cmd == 'clients':
            clients = server.get_clients()
            print(len(clients), 'clients')  
            for index, client in enumerate(clients):
                print(index, 'client inet info:', client) 
        elif cmd == 'threads':
            threads = server.get_threads()
            print(len(threads), 'threads')  
            for index, thread in enumerate(threads):
                print(index, 'thread info:', threads[thread]) 
        elif cmd == 'ctables':
            db_initializer.create_tables()
        elif cmd == 'ctriggers':
            db_initializer.create_triggers()
        elif cmd == 'initables':
            db_initializer.init_tables() 
        elif cmd == 'droptables':
            db_initializer.drop_tables()
        elif cmd == 'cltables':
            db_initializer.clear_tables()
        elif cmd == 'help':
            print(help_str)
        else:
            try:
                if cmd: 
                    sp.run(cmd.split())
            except Exception:
                print('Invalid command. Type !help for getting help')
