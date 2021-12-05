from Models.account_model import AccountModel

class Controller:
    models = {
        AccountModel: {
            'REGISTRATION ACCOUNT': 'register', 
            'SIGN IN ACCOUNT': 'sign_in', 
            'REDO ACCOUNT INFO': 'redo_info',
            'GET ACCOUNT INFO': 'get_info',
            'DELETE ACCOUNT':'delete'
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

            targetModel = None
            for model in Controller.models:
                if command in Controller.models[model]:
                    targetModel = model
            
            if targetModel:
                model = targetModel(data)
                result = eval(
                    'model.' + 
                    Controller.models[targetModel][command] + 
                    '()'
                )
                connection.send(result.encode())
            else:
                connection.send('UNKNOWN ERROR'.encode())
