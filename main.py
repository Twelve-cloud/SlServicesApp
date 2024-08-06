#!/usr/bin/env python3.10
import Database.Config.config
import subprocess as sp, sys
from threading import Thread
from Server.server import TCPServer
from Database.initializer import DbInitializer
from Controllers.dispatcher import ControllersDispatcher
from Controllers.account_controller import AccountController
from Controllers.banlist_controller import BanListController
from help import help


if __name__ == '__main__':
    db_initializer = DbInitializer()
    acc_controller = AccountController()
    banlist_controller = BanListController()
    controllers_dispatcher = ControllersDispatcher()
    server = TCPServer()
    
    mode = len(sys.argv)
    if mode == 1:
        pass
    elif mode == 2 or mode == 3:
        try:
            if mode == 2:
                server.set_inet_info(sys.argv[1], 6606)
            else:
                server.set_inet_info(sys.argv[1], int(sys.argv[2])) 
            server.turn_on()          
            dispatcher_thread = Thread(
                target = server.dispatcher, 
                args = (controllers_dispatcher.perform, ),
                daemon = True
            )
            dispatcher_thread.start()
        except Exception as error:
            print(error) 
    else:
        print('Invalid arguments from command line. Type !help for getting help')
    
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
                login = input('login: ')
                password = input('password: ')
                rolename = input('rolename: ')
                acc_controller.set_kwargs(
                    login = login, 
                    password = password,
                    rolename = rolename
                )
                result = acc_controller.add_stuff_account()
                print(result)
            case 'delete_acc':
                login = input('login: ')
                acc_controller.set_kwargs(login = login)
                result = acc_controller.delete_account()
                print(result)
            case 'update_acc':
                login = input('login: ')
                password = input('password: ')
                mob_num = input('mob_number: ')
                email = input('email: ')
                acc_controller.set_kwargs(
                    login = login,
                    password = password,
                    mob_num = mob_num,
                    email = email
                )
                result = acc_controller.edit_information()
                print(result)
            case 'read_accs':
                acc_controller.view_all_accounts()
            case 'ban_acc':
               login = input('login: ')
               started = input('started: ')
               ended = input('ended: ')
               banlist_controller.set_kwargs(
                    login = login,
                    started = started,
                    ended = ended
                )
               result = banlist_controller.ban_account()
               print(result)
            case 'unban_acc':
                login = input('login: ')
                banlist_controller.set_kwargs(login = login)
                result = banlist_controller.unban_account()
                print(result)
            case 'change_ban':
                login = input('login: ')
                started = input('started: ')
                ended = input('ended: ')
                banlist_controller.set_kwargs(
                    login = login,
                    started = started,
                    ended = ended
                )
                result = banlist_controller.change_account_ban()
                print(result)
            case 'view_bans':
                banlist_controller.view_all_bans()
            case 'help':
                help()
            case _:
                try:
                    if cmd: 
                        sp.run(cmd.split())
                except Exception:
                    print('Invalid command. Type !help for getting help')


