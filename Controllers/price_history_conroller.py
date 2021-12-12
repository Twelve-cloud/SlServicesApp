from Models.price_history_model import PriceHistoryModel
from Logger.logger import Logger

logger = Logger('logs', 'phistory_controller_logs.txt')

class PriceHistoryController:
    def __init__(self, args = None):
        if args:
            keys = [kv.split(':')[0] for kv in args]
            values = [kv.split(':')[1] for kv in args]
            self.kwargs = dict(zip(keys, values))
        self.model = PriceHistoryModel()

    def create_histogram(self):
        try:
            result = "CREATE HISTOGRAM"
            data_for_histogram = self.model.read_avg(**self.kwargs)
            history = self.model.read()
            std = []
            for x in data_for_histogram:
                prices = []
                for y in history:
                    if y.company_name == x[1]:
                        prices.append(pow(y.price - x[0], 2))
                std.append(sum(prices) ** (1/2))

            for i, data in enumerate(data_for_histogram):
                result += f'~!#$~{data[0]} [{data[1]}]:{std[i]}'
            return result
        except Exception as error:
            logger.write(f'Cannot read price average and companies, error: {error}')
            return 'CREATE HISTOGRAM FAILED'

    def get_price_history(self):
        try:
            result = "GET PRICE HISTORY SUCCESS"
            phistory = self.model.read()
            for phist in phistory:
                result += f'~!#$~Услуга: {phist.service_name}, Имя компании: {phist.company_name}, Цена: {phist.price}'
            return result
        except Exception as error:
            logger.write(f'Cannot read history, error: {error}')
            return 'GET PRICE HISTORY FAILED'  
