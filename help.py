helplist = [
    'start host, port: server starts on "host" and "port"',
    'stop: server shutdowns all connections, close all sockets and finish all threads',
    'inetinfo: returns inet information in format: "IP-adress: adress, port: port"',
    'clients: returns amount of clients and adress of every client',
    'threads: returns amount of threads and thread objects',
    'crtables: creates all tables of database',
    'drtables: drops all tables of database',
    'intables: initializes tables of database',
    'cltables: clears all tables of database',
    'crtriggers: create all triggers of database',
    'help: starts help manager',
    'another: translate command into cmd or bash what depends on os',
]

def help():
    print('Welcome to help utility!')
    print('To get a list of avaliable commands type "commands"')

    try:
        while (res := input('help> ')) != 'q':
            match res:
                case 'commands':
                    for x in helplist:
                        print(f'|\t{x}')
                case '':
                    continue
                case _:
                    print(f'No documentation for {res}')
    except Exception as e:
        print(e)


