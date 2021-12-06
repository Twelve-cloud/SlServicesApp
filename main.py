import Database.Config.config
import subprocess as sp
from threading import Thread
from Server.server import TCPServer
from Database.initializer import DbInitializer
from Controllers.dispatcher import ControllersDispatcher
from Models.account_model import AccountModel
from help import help


if __name__ == '__main__':
    db_initializer = DbInitializer()
    acc_model = AccountModel()
    server = TCPServer()
    controllers_dispatcher = ControllersDispatcher()
    
    while (cmd := input('>> ')) != 'exit':
        if cmd == '': continue

        command_args = cmd.split()
        command = command_args[0]

        match command:
            case 'start':
                if not server.is_active():
                    args = command_args[1:]
                    try:
                        host, port = args
                        port = int(port)
                
                        server.set_inet_info(host, port)
                        server.turn_on()
                
                        dispatcher_thread = Thread(
                            target = server.dispatcher, 
                            args = (controllers_dispatcher.perform, )
                        )
                        dispatcher_thread.start()
                    except Exception as e:
                        print('Invalid command. Type !help for getting help')
                else:
                    print('Server has been started yet')
            case 'stop':
                if server.is_active(): 
                    server.turn_off(dispatcher_thread)
                else:
                    print('Server has been stopped yet')
            case 'inetinfo':
                print('IP-adress: {}, port: {}'.format(*server.get_inet_info()))
            case 'clients':
                clients = server.get_clients()
                print(len(clients), 'clients')  
                for index, client in enumerate(clients):
                    print(index, 'client inet info:', clients[client]) 
            case 'threads':
                threads = server.get_threads()
                print(len(threads), 'threads')  
                for index, thread in enumerate(threads):
                    print(index, 'thread info:', threads[thread]) 
            case 'crtables':
                db_initializer.create_tables()
            case 'crtriggers':
                db_initializer.create_triggers()
            case 'intables':
                db_initializer.init_tables() 
            case 'drtables':
                db_initializer.drop_tables()
            case 'cltables':
                db_initializer.clear_tables()
            case 'create_acc':
                try:
                    login = input('login: ')
                    password = input('password: ')
                    rolename = input('rolename: ')
                    acc_model.create(login, password, rolename)
                except Exception:
                    print('Invalid command. Type !help for getting help')
            case 'delete_acc':
                try:
                    login = input('login: ')
                    acc_model.delete(login)
                except Exception:
                    print('Invalid command. Type !help for getting help')
            case 'update_acc':
                try:
                    login = input('login: ')
                    password = input('password: ')
                    mob_num = input('mob_number: ')
                    email = input('email: ')
                    acc_model.update(
                        login = login,
                        password = password,
                        mob_num = mob_num,
                        email = email
                    )
                except Exception:
                    print('Invalid command. Type !help for getting help')
            case 'read_accs':
                try:
                    accs = acc_model.read()
                    print(
                        '-' * 121, '|{:^6}|{:^20}|{:^20}|{:^20}|{:^33}|{:^16}|'.format(
                            'ID', 'LOGIN', 'PASSWORD', 'MOBILE', 'EMAIL', 'ROLENAME'),
                        '-' * 121, sep = '\n'
                    )
                    for acc in accs:
                        print(
                            '|{:^6}|{:^20}|{:^20}|{:^20}|{:^33}|{:^16}|'.format(
                                acc[0], acc[1], '', acc[3], acc[4], acc[5])
                        )
                    print('-' * 121)
                except Exception:
                    print('Invalid command. Type !help for getting help')
            case 'help':
                help()
            case _:
                try:
                    if cmd: 
                        sp.run(cmd.split())
                except Exception:
                    print('Invalid command. Type !help for getting help')

