from Models.service_model import ServiceModel
from Logger.logger import Logger

logger = Logger('logs', 'service_controller_logs.txt')

class ServiceController:
    def __init__(self, args = None):
        if args:
            keys = [kv.split(':')[0] for kv in args]
            values = [kv.split(':')[1] for kv in args]
            self.kwargs = dict(zip(keys, values))
        self.model = ServiceModel()

    def add_service(self):
        try:
            self.model.create(**self.kwargs)
            return "REQUEST SERVICES"
        except Exception as error:
            logger.write(f'Cannot add service, error: {error}')
            return 'ADD SERVICE FAILED'

    def change_service(self):
        try:
            self.model.update(**self.kwargs)
            return "REQUEST SERVICES"
        except Exception as error:
            logger.write(f'Cannot change service, error: {error}')
            return 'CHANGE SERVICE FAILED' 

    def delete_service(self):
        try:
            self.model.delete(**self.kwargs)
            return "REQUEST SERVICES"
        except Exception as error:
            logger.write(f'Cannot delete service, error: {error}')
            return 'DELETE SERVICE FAILED'


    def get_services(self):
        try:
            result = "GET SERVICE SUCCESS"
            services = self.model.read(**self.kwargs)
            for service in services:
                result += f'~!#$~{service.service_name} [{service.price}]'
            return result
        except Exception as error:
            logger.write(f'Cannot read services, error: {error}')
            return 'GET SERVICE FAILED' 


    def create_linear(self):
        try:
            result = "CREATE LINEAR"
            services = self.model.read_by_service(**self.kwargs)
            for service in services:
                result += f'~!#$~{service.company_name}:{service.price}'
            return result
        except Exception as error:
            logger.write(f'Cannot read services, error: {error}')
            return 'CREATE LINEAR FAILED'  


    def get_services_only(self):
        try:
            result = "GET SERVICES ONLY SUCCESS"
            services = self.model.read_all()
            for service in services:
                result += f'~!#$~{service.service_name}'
            return result
        except Exception as error:
            logger.write(f'Cannot read services, error: {error}')
            return 'GET SERVICE ONLY FAILED'  
