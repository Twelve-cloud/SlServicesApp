'''Contain only one class 'Logger', which writes logs to logfile'''
from os import path
from ..timer import Timer

timer = Timer()

class Logger:
    '''
        Class Logger represents log writer.
        Params description:
        1. filename - name of logfile
        2. path - path to logfile
    '''
    def __init__(self, path: str, filename: str):
        self.path = path
        self.filename = filename

    def write(logdata: str):
        try:
            file_with_path = path.join(self.path, self.filename)
            file = open(file_with_path, 'a')
            file.write(logdata + '\n')
        except Exception:
            logger_file = open('logger.txt', 'a')
            logger_file.write(
                f'Error with write log data into file "'
                f'{self.filename}" placed in "{self.path} "'
                f'at {timer.now()}'
            )
            logger_file.close()
        finally:
            file.close()

        
