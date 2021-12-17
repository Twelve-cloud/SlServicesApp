from .account_controller import AccountController
from .basket_controller import BasketController
from .company_controller import CompanyController
from .service_controller import ServiceController
from .price_history_conroller import PriceHistoryController

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
            'GET ORDERS': 'get_orders'
        },
        CompanyController: {
            'ADD COMPANY': 'add_company',
            'DELETE COMPANY': 'delete_company',
            'CHANGE COMPANY': 'change_company',
            'GET COMPANY': 'get_companies'
        },
        ServiceController: {
            'ADD SERVICE': 'add_service',
            'DELETE SERVICE': 'delete_service',
            'CHANGE SERVICE': 'change_service',
            'GET SERVICE': 'get_services',
            'CREATE LINEAR': 'create_linear',
            'GET SERVICES ONLY': 'get_services_only',
            'GET DATA FOR HISTOGRAM': 'get_data_for_histogram',
            'GET AVG PRICE AND SERVICE': 'get_avg_price_and_service'
        },
        PriceHistoryController: {
            'CREATE HISTOGRAM': 'create_histogram',
            'GET PRICE HISTORY': 'get_price_history'
        }
    }

    def perform(self, connection, server):
        while True:
            size_bytes = connection.recv(16)
            size = int.from_bytes(size_bytes, 'little', signed = False)
            message_encoded = connection.recv(size)
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
                if command == 'ADD BASKET' or command == 'DELETE BASKET' or command == 'ADD COMPANY' \
                    or command == 'DELETE COMPANY' or command == 'CHANGE COMPANY' or command == 'ADD SERVICE' \
                    or command == 'DELETE SERVICE' or command == 'CHANGE SERVICE':
                    clients = server.get_clients()
                    for client in clients:
                        client.send(result.encode())
                else:
                    connection.send(result.encode())
            else:
                connection.send('UNKNOWN ERROR'.encode())


