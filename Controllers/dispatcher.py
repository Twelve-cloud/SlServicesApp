from .account_controller import AccountController

class ControllersDispatcher:
    controllers = {
        AccountController: {
            'REGISTRATION ACCOUNT': 'register_account', 
            'SIGN IN ACCOUNT': 'sign_in', 
            'REDO ACCOUNT INFO': 'edit_information',
            'GET ACCOUNT INFO': 'get_information',
            'DELETE ACCOUNT':'delete_account'
        },
    }

    def perform(self, connection, server):
        while True:
            message_encoded = connection.recv(4096)
            message = message_encoded.decode()

            if not message:
                break

            if message == 'EXIT':
                server.del_thread(connection)
                server.del_client(connection)
                connection.close()
                break

            data_list = message.split('~!#$~')
            command, data = data_list[0], data_list[1:]

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
                connection.send(result.encode())
            else:
                connection.send('UNKNOWN ERROR'.encode())
