from Models.company_model import CompanyModel
from Logger.logger import Logger

logger = Logger('logs', 'company_controller_logs.txt')

class CompanyController:
    def __init__(self, args = None):
        if args:
            keys = [kv.split(':')[0] for kv in args]
            values = [kv.split(':')[1] for kv in args]
            self.kwargs = dict(zip(keys, values))
        self.model = CompanyModel()

    def add_company(self):
        try:
            company_name = self.kwargs.pop('company_name')
            self.model.create(company_name)
            return "REQUEST COMPANIES"
        except Exception as error:
            logger.write(f'Cannot add company, error: {error}')
            return 'ADD COMPANY FAILED'

    def change_company(self):
        try:
            company_name = self.kwargs.pop('company_name')
            old_name = self.kwargs.pop('old_name')
            self.model.update(old_name, company_name)
            return "REQUEST COMPANIES"
        except Exception as error:
            logger.write(f'Cannot change company, error: {error}')
            return 'CHANGE COMPANY FAILED' 

    def delete_company(self):
        try:
            company_name = self.kwargs.pop('company_name')
            self.model.delete(company_name)
            return "REQUEST COMPANIES"
        except Exception as error:
            logger.write(f'Cannot delete company, error: {error}')
            return 'DELETE COMPANY FAILED'


    def get_companies(self):
        try:
            result = "GET COMPANY SUCCESS"
            companies = self.model.read()
            for company in companies:
                result += f'~!#$~{company.company_name}'
            return result
        except Exception as error:
            logger.write(f'Cannot read companies, error: {error}')
            return 'GET COMPANY FAILED' 
            
