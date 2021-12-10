from .account_controller import AccountController
from .basket_controller import BasketController

class ControllersDispatcher:
    controllers = {
        AccountController: {
            'REGISTRATION ACCOUNT': 'register_account', 
            'SIGN IN ACCOUNT': 'sign_in', 
            'REDO ACCOUNT INFO': 'edit_information',
            'GET ACCOUNT INFO': 'get_information',
            'DELETE ACCOUNT':'delete_account'
        },
        BasketController: {
            'GET BASKET': 'get_basket',
            'ADD BASKET': 'add_basket',
            'DELETE BASKET': 'delete_basket',
        },
    }

    def perform(self, connection, server):
        while True:
            size_bytes = connection.recv(4)
            size = int.from_bytes(size_bytes, 'little', signed = False)
            print(size)
            message_encoded = connection.recv(size)
            message = message_encoded.decode()

            print(message)

            if not message:
                break

            if message == 'EXIT':
                server.del_thread(connection)
                server.del_client(connection)
                connection.close()
                break

            data_list = message.split('~!#$~')
            command, data = data_list[0], data_list[1:]

            if command == 'START CHAT' or command == 'MESSAGE' or command == 'FINISH CHAT':
                clients = server.get_clients()
                for client in clients:
                    client.send(message.encode())
                continue

            targetController = None
            for controller in ControllersDispatcher.controllers:
                if command in ControllersDispatcher.controllers[controller]:
                    targetController = controller
            
            if targetController:
                controller = targetController(data)
                result = eval(
                    'controller.' + 
                    ControllersDispatcher.controllers[targetController][command] + 
                    '()'
                )
                if command == 'ADD BASKET' or command == 'DELETE BASKET':
                    clients = server.get_clients()
                    for client in clients:
                        client.send(result.encode())
                else:
                    connection.send(result.encode())
            else:
                connection.send('UNKNOWN ERROR'.encode())

