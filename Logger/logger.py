from os import path
from Timer.timer import Timer

timer = Timer()

class Logger:
    def __init__(self, path, filename):
        self.path = path
        self.filename = filename

    def write(self, logdata):
        try:
            file_with_path = path.join(self.path, self.filename)
            file = open(file_with_path, 'a')
            file.write(f'{logdata} at {timer.now()}\n')
            file.close()
        except Exception:
            lfile_with_path = path.join('logs', 'logger.txt')
            logger_file = open(lfile_with_path, 'a')
            logger_file.write(
                f'Error with write log data into file "'
                f'{self.filename}" placed in "{self.path}" '
                f'at {timer.now()}\n'
            )
            logger_file.close()

