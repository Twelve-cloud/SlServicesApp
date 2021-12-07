from Models.banlist_model import BanListModel
from Logger.logger import Logger

logger = Logger('logs', 'banlist_controller_logs.txt')

class BanListController:
    def __init__(self):
        self.model = BanListModel()

    def set_kwargs(**kwargs):
        self.kwargs = kwargs

    def ban_account(self):
        pass 

    def unban_account(self):
        pass

    def change_account_ban(self):
        pass

    def view_all_bans(self):
        try:
            bans = self.model.read()
            print(
                '-' * 83, '|{:^6}|{:^20}|{:^26}|{:^26}|'.format(
                    'ID', 'ACC_ID', 'STARTED', 'ENDED'),
                '-' * 83, sep = '\n'
            )
            for ban in bans:
                print(
                    '|{:^6}|{:^20}|{:^26}|{:^26}|'.format(
                        ban[0], ban[1], str(ban[2]), str(ban[3]))
                )
            print('-' * 83)
        except Exception as error:
            logger.write(f'Cannot select ban from database, error: {error}')
            print('CANNOT READ DATA FROM DATABASE')
    
