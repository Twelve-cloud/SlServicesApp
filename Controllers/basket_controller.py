import time
from Models.basket_model import BasketModel
from Controllers.account_controller import AccountController
from Logger.logger import Logger

logger = Logger('logs', 'basket_controller_logs.txt')

class BasketController:
    def __init__(self, args = None):
        if args:
            keys = [kv.split(':')[0] for kv in args]
            values = [kv.split(':')[1] for kv in args]
            self.kwargs = dict(zip(keys, values))
        self.model = BasketModel()
        self.account_controller = AccountController()

    def get_basket(self):
        try:
            result = "GET BASKET SUCCESS"
            type = self.kwargs['type']
            baskets = self.model.read()
            for basket in baskets:
                if basket.type == type:
                    result += f'~!#$~{basket.name} [{basket.time}]'
            return result
        except Exception as error:
            logger.write(f'Cannot read basket, error: {error}')
            return 'GET BASKET FAILED' 

    def get_orders(self):
        try:
            result = "GET ORDERS SUCCESS"
            type = self.kwargs['type']
            baskets = self.model.read()
            for basket in baskets:
                if basket.type == type:
                    self.account_controller.set_kwargs(id = basket.acc_id)
                    login = self.account_controller.get_login_by_id()
                    result += f'~!#$~{login}: {basket.name} [{basket.time}]'
            return result
        except Exception as error:
            logger.write(f'Cannot read basket, error: {error}')
            return 'GET ORDERS FAILED'  

    def add_basket(self):
        try:   
            login = self.kwargs.pop('login')
            self.account_controller.set_kwargs(login = login)
            acc_id = self.account_controller.get_id_by_login()
            self.model.create(acc_id, **self.kwargs)
            return 'REQUEST AGAIN'
        except Exception as error:
            logger.write(f'Cannot add basket, error: {error}')
            return 'ADD BASKET FAILED'

    def delete_basket(self):
        try:
            login = self.kwargs.pop('login')
            self.account_controller.set_kwargs(login = login)
            acc_id = self.account_controller.get_id_by_login()
            self.model.delete(acc_id, **self.kwargs)
            return 'REQUEST AGAIN'
        except Exception as error:
            logger.write(f'Cannot delete basket, error: {error}')
            return 'DELETE BASKET FAILED'
