from Models.account_model import AccountModel

class Controller:
    models = {
            AccountModel: {'REGISTRATION ACCOUNT': 'register', 'SIGN IN ACCOUNT': 'sign_in', 'REDO ACCOUNT INFO': 'redo_info', 'GET ACCOUNT INFO': 'get_info', 'DELETE ACCOUNT':'delete'}
            }

    def perform(self, connection, thread_state):
        while thread_state.is_active():
            message_encoded = connection.recv(4096)
            message = message_encoded.decode()
            data_list = message.split('~!#$~')
            command, data = data_list[0], data_list[1:]

            targetModel = None
            for model in Controller.models:
                if command in Controller.models[model]:
                    targetModel = model(data)

            if targetModel:
                result = eval('targetModel.' + Controller.models[targetModel][command]())
                connection.send(result.encode())
            else:
               connection.send('UNKNOWN ERROR'.encode()) 

'''
class ControllerDispatcher:
    controllers = {
            AccountController: ['REGISTRATION ACCOUNT', 'SIGN IN ACCOUNT', 'REDO ACCOUNT INFO', 'GET ACCOUNT INFO', 'DELETE ACCOUNT']
            }

    def dispatch(self, connection, thread_state):
        while thread_state.is_active():
            message_encoded = connection.recv(4096)
            message = message_encoded.decode()
            data_list = message.split('~!#$~')
            command, data = data_list[0], data_list[1:]

            targetController = None
            for controller in ControllerDispatcher.controllers:
                if command in ControllerDispatcher.controllers[controller]:
                    targetController = controller(data)
            
            if targetController: 
                result = targetController.change_model()
                connection.send(result.encode())
            else:
                connection.send('UNKNOWN ERROR'.encode())
                
'''
