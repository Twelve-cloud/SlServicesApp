from Models

class Controller:
    models = {
            'REGISTRATION ACCOUNT': [AccountModel, register], 
            'SIGN IN ACCOUNT': [AccountModel, sign_in],
            'REDO ACCOUNT_INFO': [AccountModel, redo_info],
            'GET ACCOUNT_INFO': [AccountModel, get_info],
            'DELETE ACCOUNT': [AccountModel, delete],
            }

    def perform(self, connection, thread_state):
        while thread_state.is_active():
            message_encoded = connection.recv(4096)
            message = message_encoded.decode('utf-8').split('~!#$~')
            command, data = message[0], message[1:]

            if models.get(command, False): 
                model = models[command][0]
                result = model.models[command][1](data)
                connection.send(result)
            else:
                connection.send('UNKNOWN ERROR')
