'''Contain only one class 'Timer', which execute different functions with time'''
import time

class Timer:
    '''
        Class 'Timer' represents package of functions to work with time
        Class contains function 'now' to get current time
        '''
    def now(self) -> str:
        '''Return time in format "Weekday Month Day Time Year"'''
        return time.ctime(time.time())
